from django.db import models
from django.contrib.auth.models import User

# user와 1:1로 연결
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

# 자유게시판
class Post(models.Model):
    postname = models.CharField(max_length=50)
    # 게시글 Post에 이미지 추가
    mainphoto = models.ImageField(blank=True, null=True)
    contents = models.TextField()
    # 작성자
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # 기존 데이터 NULL 허용

    # postname이 Post object 대신 나오기
    def __str__(self):
        return self.postname
    
# 정보게시판
class infoPost(models.Model):
    postname = models.CharField(max_length=50)
    # 게시글 Post에 이미지 추가
    mainphoto = models.ImageField(blank=True, null=True)
    contents = models.TextField()

    # postname이 Post object 대신 나오기
    def __str__(self):
        return self.postname