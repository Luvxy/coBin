from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Post
from django.contrib.auth.forms import AuthenticationForm  # Django 내장 로그인 폼
from django.shortcuts import render, get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.paginator import Paginator

# webhook 함수에 필요한 라이브러리
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

import firebase_admin
from firebase_admin import credentials, firestore
from cobin_app.forms import UserForm

import os
from django.conf import settings

# Firebase 인증 정보 로드
cred_path = settings.FIREBASE_CREDENTIALS
if not os.path.exists(cred_path):
    raise FileNotFoundError(f"Firebase credential file not found: {cred_path}")

cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

# Firestore 인스턴스 생성
db = firestore.client()

def save_user_to_firestore(user_id, name, email, membership):
    user_ref = db.collection("users").document(user_id)
    user_ref.set({
        "name": name,
        "email": email,
        "membership": membership,
        "profileImage": ""
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

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})

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
def contact(request):
    return render(request, 'contact.html')  # index 파일 경로

@login_required
def blog(request):
    search_query = request.GET.get('search', '')  # 검색어 가져오기
    postlist = Post.objects.select_related('author').all().order_by('-id')  # 최신순 정렬

    if search_query:
        postlist = postlist.filter(postname__icontains=search_query)  # 제목에 검색어 포함된 글만 필터링

    paginator = Paginator(postlist, 10)  # 10개씩 페이지 나누기
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog.html', {'page_obj': page_obj, 'search_query': search_query})

# blog의 게시글(posting)을 부르는 posting 함수
@login_required
def posting(request, pk):
    # 게시글(Post) 중 pk(primary_key)를 이용해 하나의 게시글(post)를 검색
    post = Post.objects.get(pk=pk)
    # posting.html 페이지를 열 때, 찾아낸 게시글(post)을 post라는 이름으로 가져옴
    return render(request, 'posting.html', {'post':post})

@login_required
def new_post(request):
    if request.method == 'POST':
        if request.POST['mainphoto']:
            new_article=Post.objects.create(
                postname=request.POST['postname'],
                contents=request.POST['contents'],
                mainphoto=request.POST['mainphoto'],
            )
        else:
            new_article=Post.objects.create(
                postname=request.POST['postname'],
                contents=request.POST['contents'],
                mainphoto=request.POST['mainphoto'],
            )
        return redirect('/blog/')
    return render(request, 'new_post.html')

@login_required
def remove_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('/blog/')
    return render(request, 'remove_post.html', {'post': post})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # 폼 객체 생성
        if form.is_valid():  # 폼 유효성 검사
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)  # 사용자 인증

            if user is not None:
                login(request, user)  # 로그인
                return redirect('some_view')  # 로그인 후 리디렉션
            else:
                # ... 인증 실패 처리 ...
                pass  # form.errors에 에러 메시지가 자동으로 추가됨
        else:
            # ... 폼 유효성 검사 실패 ...
            pass # form.errors에 에러 메시지가 자동으로 추가됨

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