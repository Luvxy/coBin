from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import *
from django.contrib.auth.forms import AuthenticationForm  # Django 내장 로그인 폼
from django.shortcuts import render, get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.db.models import F
from django.http import HttpResponseForbidden

# api 관련 라이브러리
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# webhook 함수에 필요한 라이브러리
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# email verification 함수에 필요한 라이브러리
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.crypto import get_random_string
from .models import UserProfile
import random
import requests

# firebase 관련 라이브러리
import firebase_admin
from firebase_admin import credentials, firestore
from cobin_app.forms import UserForm

# 웹소켓 관련
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import os
from datetime import datetime
from django.conf import settings

# Firebase 인증 정보 로드
cred_path = settings.FIREBASE_CREDENTIALS
if not os.path.exists(cred_path):
    raise FileNotFoundError(f"Firebase credential file not found: {cred_path}")

cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

# Firestore 인스턴스 생성
db = firestore.client()

def save_user_to_firestore(user_id, name, email, membership, point1=0, point2=0):
    user_ref = db.collection("users").document(user_id)
    user_ref.set({
        "name": name,
        "email": email,
        "membership": membership,
        "profileImage": "",
        "point1": point1,
        "point2": point2,
        "profileImage": "/media/default_profile.png"
    })
    
def set_user_image_to_firestore(user_id, image_url):
    user_ref = db.collection("users").document(user_id)
    user_ref.update({
        "profileImage": image_url
    })
    
def set_user_membership_to_firestore(user_id, membership):
    user_ref = db.collection("users").document(user_id)
    user_ref.update({
        "membership": membership
    })

def get_user_from_firestore(user_id):
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        return user_doc.to_dict()
    else:
        return None

def update_user_points(user_id, new_points):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {
            "type": "send_point_update",
            "message": {"points": new_points}
        }
    )
    
@csrf_exempt
def purchase_points(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')  # 사용자 이름
            points_to_add = data.get('points')  # 구매한 포인트

            # 사용자 포인트 업데이트
            user = User.objects.get(username=username)  # username으로 사용자 조회
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.point1 = (profile.point1 or 0) + points_to_add
            profile.save()

            # Firebase에서 기존 문서 업데이트
            user_ref = db.collection("users").document(username)  # username을 문서 ID로 사용
            user_ref.update({
                "point1": profile.point1,
                "point2": profile.point2 or 0
            })

            # 구매 기록 추가
            purchase_ref = user_ref.collection("purchaseHistory")
            purchase_ref.add({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # 현재 날짜와 시간
                "points": points_to_add,
                "description": f"{points_to_add} 포인트 구매"
            })

            # WebSocket을 통해 프로그램으로 포인트 업데이트 알림 전송
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{username}",  # WebSocket 그룹 이름
                {
                    "type": "send_point_update",
                    "message": {
                        "point1": profile.point1,
                        "point2": profile.point2 or 0
                    }
                }
            )

            return JsonResponse({"status": "success", "message": "포인트가 성공적으로 추가되었습니다."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request method."})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_consumed_points(request):
    """
    클라이언트에서 소모된 포인트를 서버에 전송하여 업데이트하는 API
    """
    try:
        print(f"Request method: {request.method}")  # 요청 메서드 출력
        print(f"Request path: {request.path}")  # 요청 URL 출력
        print(f"Authenticated user: {request.user}")  # 디버깅용
        print(f"Username: {request.user.username}")  # 디버깅용

        data = request.data
        consumed_point1 = data.get('consumed_point1', 0)
        consumed_point2 = data.get('consumed_point2', 0)

        # 사용자 포인트 업데이트
        user = User.objects.get(username=request.user.username)
        profile, created = UserProfile.objects.get_or_create(user=user)

        # 포인트 차감
        profile.point1 = max((profile.point1 or 0) - consumed_point1, 0)
        profile.point2 = max((profile.point2 or 0) - consumed_point2, 0)
        profile.save()

        # Firebase에서 기존 문서 업데이트
        user_ref = db.collection("users").document(request.user.username)
        user_ref.update({
            "point1": profile.point1,
            "point2": profile.point2
        })

        return JsonResponse({"status": "success", "message": "포인트가 성공적으로 업데이트되었습니다."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

@login_required
def profile_view(request):
    user_id = str(request.user.username)  # Django 유저 ID를 문자열로 변환 (Firebase UID와 일치해야 함)
    
    # Firestore에서 사용자 정보 가져오기
    user_data = get_user_from_firestore(user_id)
    
    if not user_data:
        return redirect('logout')  # Firebase에 사용자 정보가 없으면 로그아웃 처리

    # Firestore에서 투자 기록 가져오기
    investment_ref = db.collection("users").document(user_id).collection("investmentHistory")
    investment_data = investment_ref.stream()  # Firestore에서 데이터 가져오기

    profit_data = []
    for doc in investment_data:
        data = doc.to_dict()
        profit_data.append({
            "date": data.get("date"),
            "amount": data.get("amount"),
            "profitRate": data.get("profitRate")
        })

    # 날짜순 정렬
    profit_data.sort(key=lambda x: x["date"])

    # Firestore에서 활동 로그 가져오기
    act_log_ref = db.collection("users").document(user_id).collection("actLog").limit(5)
    act_log_data = act_log_ref.stream()
    
    # 활동 로그는 최대 10개까지만 가져오기
    

    user_acting_log = []
    for doc in act_log_data:
        data = doc.to_dict()
        user_acting_log.append({
            "date": data.get("date"),
            "type": data.get("type"),
            "address": data.get("address")
        })

    # 날짜순 정렬
    user_acting_log.sort(key=lambda x: x["date"], reverse=True)  # 최신 로그가 위로 오도록 정렬

    return render(request, "profile.html", {
        "profit_data": profit_data,
        "user_data": user_data,
        "user_acting_log": user_acting_log
    })


###################################################################################################
# cobin app api
###################################################################################################

# cobin app api connet
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_api(request):
    return Response({"message": "API 접근 성공", "user": request.user.username})

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            save_user_to_firestore(user.username, user.username, user.email, "basic")
            print("회원가입 성공")
            return redirect('/')
    else:
        print("회원가입 실패")
        form = UserForm()
    return render(request, 'login.html', {'form': form})


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def get_user_info(request):
    """유저 정보를 반환하는 API"""
    user = request.user
    user_data = {
        "username": user.username,
        "email": user.email,
    }
    return Response(user_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def get_user_by_id(request, user_id):
    """
    요청으로 받은 user_id를 사용하여 Firebase Firestore에서 유저 정보를 반환하는 API
    """
    try:
        # Firestore에서 유저 정보 가져오기
        user_ref = db.collection("users").document(user_id)
        user_doc = user_ref.get()

        if user_doc.exists:
            user_data = user_doc.to_dict()
            return Response({
                "status": "success",
                "user_data": user_data
            }, status=200)
        else:
            return Response({
                "status": "fail",
                "message": f"User with ID '{user_id}' not found."
            }, status=404)
    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=500)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def upload_inv(request, user_id):
    """
    API로 받은 데이터를 Firebase Firestore에 저장
    """
    try:
        # 요청 데이터에서 date, amount, profitRate 가져오기
        data = request.data
        date = data.get('date')  # "2025/03/28" 형식
        amount = data.get('amount')
        profit_rate = data.get('profitRate')

        # 필수 데이터가 없는 경우 에러 반환
        if not date or amount is None or profit_rate is None:
            return Response({
                "status": "fail",
                "message": "date, amount, and profitRate are required."
            }, status=400)

        # 날짜 형식을 "YYYYMMDD"로 변환
        formatted_date = date.replace("/", "")  # "20250328"

        # Firestore에서 기존 문서 수를 가져와 count 계산
        user_ref = db.collection("users").document(user_id).collection("investmentHistory")
        existing_docs = user_ref.stream()
        count = sum(1 for _ in existing_docs) + 1  # 기존 문서 수 + 1

        # 문서 이름 생성: "YYYYMMDD_count"
        document_id = f"{formatted_date}_{count}"

        # Firestore에 데이터 저장
        user_ref.document(document_id).set({
            "date": date,
            "amount": amount,
            "profitRate": profit_rate
        })

        return Response({
            "status": "success",
            "message": "Data uploaded successfully.",
            "document_id": document_id
        }, status=201)
    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=500)
    

###################################################################################################
# cobin app api end line
###################################################################################################


# email verification 함수
@login_required
def send_email_verification(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)  # ✅ UserProfile 자동 생성

    verification_code = get_random_string(length=6, allowed_chars='0123456789')
    profile.email_verification_code = verification_code
    profile.save()

    send_mail(
        '이메일 인증 코드',
        f'인증 코드: {verification_code}',
        'no-reply@yourdomain.com',
        [user.email],
        fail_silently=False,
    )

    messages.success(request, "이메일로 인증 코드가 발송되었습니다.")
    return redirect('profile')

@login_required
def verify_email(request):
    if request.method == "POST":
        code = request.POST.get('code')
        profile, created = UserProfile.objects.get_or_create(user=request.user)  # ✅ UserProfile 자동 생성

        if profile.email_verification_code == code:
            profile.email_verified = True
            profile.save()
            messages.success(request, "이메일 인증이 완료되었습니다.")
        else:
            messages.error(request, "인증 코드가 틀립니다.")

        return redirect('profile')

#문자 인증
# 휴대전화(SMS) 인증
@login_required
def send_sms_verification(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    verification_code = str(random.randint(100000, 999999))
    profile.sms_verification_code = verification_code
    profile.save()

    # SMS API를 이용한 인증 코드 전송 (Twilio 예제)
    requests.post(
        "https://api.twilio.com/2010-04-01/Accounts/YOUR_ACCOUNT_SID/Messages.json",
        data={
            "To": profile.phone_number,
            "From": "YOUR_TWILIO_NUMBER",
            "Body": f"인증 코드: {verification_code}"
        },
        auth=("YOUR_ACCOUNT_SID", "YOUR_AUTH_TOKEN")
    )

    messages.success(request, "휴대전화로 인증 코드가 발송되었습니다.")
    return redirect('profile')

@login_required
def verify_sms(request):
    if request.method == "POST":
        code = request.POST.get('code')
        profile, created = UserProfile.objects.get_or_create(user=request.user)

        if profile.sms_verification_code == code:
            profile.phone_verified = True
            profile.save()
            messages.success(request, "휴대전화 인증이 완료되었습니다.")
        else:
            messages.error(request, "인증 코드가 틀립니다.")

    return redirect('profile')

@login_required
def post_list(request, category):
    posts = Post.objects.filter(category=category).order_by('-created_at')
    search_query = request.GET.get('search', '')
    if search_query:
        posts = posts.filter(title__icontains=search_query)

    context = {
        'page_obj': posts,  # 페이징 대신 전체 리스트 전달
        'category': category,
        'search_query': search_query
    }
    
    return render(request, 'blog.html', context)

@csrf_exempt  # CSRF 보호 비활성화 (웹훅은 보통 CSRF 토큰을 사용하지 않음)
def webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # 웹훅 데이터 파싱
            print("웹훅 데이터:", data)

            # 웹훅 데이터 처리 로직
            # ... (예: 데이터베이스 저장, 다른 시스템 연동 등)

            return JsonResponse({"status": "success"})  # 성공 응답
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)
        except Exception as e:
            print("웹훅 처리 오류:", e)
            return JsonResponse({"status": "error", "message": "Webhook processing failed"}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

@login_required
def profile(request):
    user_id = request.user.username  # Django User.username을 고유 식별자로 사용
    user_data = get_user_from_firestore(user_id)  # Firestore에서 가져오는 함수 (이미 존재)

    return render(request, 'profile.html', {
        'user_data': user_data
    })

@login_required
def home(request):
    postlist = Post.objects.all()
    return render(request, 'index.html', {'postlist':postlist})  # index 파일 경로

@login_required
def download(request):
    return render(request, 'download.html')  # download 파일 경로

def purchase(request):
    points = [480 * i for i in range(3, 10)]  # 480 ~ 4320 포인트
    return render(request, 'purchase.html', {'points': points})

@login_required
def best(request):
    return render(request, 'best.html')  # index 파일 경로

@login_required
def contact(request):
    return render(request, 'contact.html')  # index 파일 경로

@login_required
def blog(request):
    search_query = request.GET.get('search', '')  # 검색어 가져오기
    postlist = Post.objects.select_related('author').all().order_by('-id')  # 최신순 정렬

    if search_query:
        postlist = postlist.filter(postname__icontains=search_query)  # 제목에 검색어 포함된 글만 필터링

    paginator = Paginator(postlist, 50)  # 10개씩 페이지 나누기
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog.html', {'page_obj': page_obj, 'search_query': search_query})

@login_required
def post_detail(request, category, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    # 댓글 작성 처리
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
        return redirect('post_detail', category=category, pk=pk)

    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'posting.html', context)

# blog의 게시글(posting)을 부르는 posting 함수
@login_required
def posting(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 해당 유저가 이 포스트를 조회했는지 확인
    has_viewed = PostView.objects.filter(user=request.user, post=post).exists()

    if not has_viewed:
        # 조회수 +1
        post.view_count += 1
        post.save()

        # 조회 기록 저장
        PostView.objects.create(user=request.user, post=post)

    # 조회수 최신화
    post.refresh_from_db()
    if request.method == 'POST':
        # form에서 name="content"로 댓글 내용을 받아옴
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
        return redirect('posting', pk=pk)
    
    return render(request, 'posting.html', {'post': post})

@login_required
def like(request, category, pk):
    post = get_object_or_404(Post, pk=pk, category=category)

    if request.user in post.liked_users.all():
        post.liked_users.remove(request.user)
    else:
        post.liked_users.add(request.user)

    return redirect('post_detail', category=category, pk=pk)

@login_required
def new_post(request, category):
    if request.method == 'POST':
        new_article = Post.objects.create(
            postname=request.POST['postname'],
            contents=request.POST['contents'],
            mainphoto=request.FILES.get('mainphoto'),
            author=request.user,
            category=category  # 카테고리 저장
        )
        return redirect('post_list', category=category)
    return render(request, 'new_post.html', {'category': category})

@login_required
def delete_post(request, category, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        return HttpResponseForbidden("권한이 없습니다.")

    post.delete()
    return redirect('post_list', category=category)

@login_required
def delete_comment(request, category, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.user != comment.author:
        return HttpResponseForbidden("권한이 없습니다.")

    comment.delete()
    return redirect('post_detail', category=category, pk=post_pk)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # 폼 객체 생성
        if form.is_valid():  # 폼 유효성 검사
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)  # 사용자 인증

            if user is not None:
                profile, created = UserProfile.objects.get_or_create(user=user)  # ✅ UserProfile 자동 생성

            if not (profile.email_verified and profile.phone_verified):
                messages.error(request, "이메일과 휴대전화 인증을 완료해야 합니다.")
                return redirect('profile')

            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "아이디 또는 비밀번호가 잘못되었습니다.")

    else:
        form = AuthenticationForm()  # 빈 폼 객체 생성

    return render(request, 'login.html', {'form': form})  # 폼 객체를 템플릿에 전달

@csrf_exempt
@login_required
def upload_user_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        user_id = request.user.username

        # 파일 확장자 유지하면서 저장
        file_path = f"profile_images/{user_id}_{image_file.name}"
        file_name = default_storage.save(file_path, ContentFile(image_file.read()))

        # 저장된 이미지의 URL 생성
        image_url = f"{settings.MEDIA_URL}{file_name}"

        # Firestore에 저장 (기존 set_user_image_to_firestore 함수 사용)
        set_user_image_to_firestore(user_id, image_url)

        return JsonResponse({'status': 'success', 'image_url': image_url})
    else:
        return JsonResponse({'status': 'fail', 'reason': 'No image provided'}, status=400)