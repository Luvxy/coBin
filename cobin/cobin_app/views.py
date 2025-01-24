from django.shortcuts import render

def home(request):
    return render(request, 'index.html')  # 템플릿 파일 경로
