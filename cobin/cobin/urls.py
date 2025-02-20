"""cobin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cobin_app import views
from django.shortcuts import render

# 이미지를 업로드 하기 위한 설정
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

app_name = 'cobin_app'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: render(request, 'index.html')),  # 기본 페이지
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:pk>/', views.posting, name="posting"),
    path('blog/new_post/', views.new_post),
    path('blog/<int:pk>/remove/', views.remove_post),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('webhook/', views.webhook, name='webhook'),
    path('blog/<int:post_id>/', views.post_detail, name='post_detail'),
    path('upload_user_image/', views.upload_user_image, name='upload_user_image'),
    path('blog/<int:pk>/like/', views.like, name='like'),
]

# 이미지 URL 설정
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)