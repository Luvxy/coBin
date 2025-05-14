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
from django.conf.urls import handler404, handler500

# 이미지를 업로드 하기 위한 설정
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'cobin_app'
handler404 = 'cobin_app.views.custom_404'
handler500 = 'cobin_app.views.custom_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: render(request, 'index.html')),  
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('contact/', views.contact, name='contact'),
    path('upload_user_image/', views.upload_user_image, name='upload_user_image'),
    path('profile/', views.profile_view, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('webhook/', views.webhook, name='webhook'),
    path('best/', views.best, name='best'),
    path('download/', views.download, name='download'),
    path('purchase/', views.purchase, name='purchase'),
    path('search/', views.search, name='search'),
    path('chart/', views.chart, name='chart'),
    
    # 게시판 URL
    path('blog/', views.blog, name='blog'),
    path('blog/<str:category>/', views.post_list, name='post_list'),
    path('blog/<str:category>/new_post/', views.new_post, name='new_post'),  # ✅ 수정된 부분
    path('blog/<str:category>/<int:pk>/', views.post_detail, name='post_detail'),
    path('blog/<str:category>/<int:pk>/like/', views.like, name='like'),
    path('blog/<str:category>/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('blog/<str:category>/<int:pk>/update-status/', views.update_post_status, name='update_post_status'),
    path('api/user/update_consumed_points/', views.update_consumed_points, name='update_consumed_points'),
    
    # cobin app 관련 URL
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('protected-api/', views.protected_api, name='protected_api'),
    path('api/user-info/', views.get_user_info, name='get_user_info'),
    path('api/user/<str:user_id>/', views.get_user_by_id, name='get_user_by_id'),
    path('api/user/<str:user_id>/upload_inv/', views.upload_inv, name='upload_inv'),
    path('purchase-points/', views.purchase_points, name='purchase_points'),
    path('api/user/update_consumed_points/', views.update_consumed_points, name='update_consumed_points'),
    path('api/email/send/', views.send_email, name='send_email'),
    
    # emali
    path('send-email-verification/', views.send_email_verification, name='send_email_verification'),
    path('verify-email/', views.verify_email, name='verify_email'),
    
    # 휴대전화(SMS) 인증
    path('verify/sms/send/', views.send_sms_verification, name='send_sms_verification'),
    path('verify/sms/', views.verify_sms, name='verify_sms'),
    
    # Ai 관련
    path("chat/", views.chat_view, name="ai_chat_page"),
    path("chat/send/", views.ai_chat, name="ai_chat"),  # 폼 action 대상
]

# 이미지 URL 설정
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)