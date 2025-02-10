from django.shortcuts import render
from django.shortcuts import redirect
from .models import Post

import firebase_admin
from firebase_admin import credentials, firestore

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

def profile(request):
    user_id = "user123"  # 예제 유저 ID
    user_ref = db.collection("users").document(user_id)
    user = user_ref.get().to_dict()
    return render(request, 'profile.html', {'user_data': user})

def home(request):
    return render(request, 'index.html')  # index 파일 경로

def contact(request):
    return render(request, 'contact.html')  # index 파일 경로

def profile(request):
    return render(request, 'profile.html')  # index 파일 경로

def blog(request):
    # 게시글을 전부 가져와 postlist에 저장
    postlist = Post.objects.all()
    # blog.html 파일을 불러올때 postlist도 같이 불러옴
    return render(request, 'blog.html', {'postlist':postlist})  # blog 파일 경로

# blog의 게시글(posting)을 부르는 posting 함수
def posting(request, pk):
    # 게시글(Post) 중 pk(primary_key)를 이용해 하나의 게시글(post)를 검색
    post = Post.objects.get(pk=pk)
    # posting.html 페이지를 열 때, 찾아낸 게시글(post)을 post라는 이름으로 가져옴
    return render(request, 'posting.html', {'post':post})

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

def remove_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('/blog/')
    return render(request, 'remove_post.html', {'post': post})

def save_user_to_firestore(user_id, name, email, membership):
    user_ref = db.collection("users").document(user_id)
    user_ref.set({
        "name": name,
        "email": email,
        "membership": membership,
        "profileImage": ""
    })

def get_user_from_firestore(user_id):
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        return user_doc.to_dict()
    else:
        return None
