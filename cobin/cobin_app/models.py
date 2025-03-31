from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # 휴대전화 번호
    email_verified = models.BooleanField(default=False)  # 이메일 인증 여부
    phone_verified = models.BooleanField(default=False)  # 휴대전화 인증 여부
    email_verification_code = models.CharField(max_length=6, blank=True, null=True)  # 이메일 인증 코드
    sms_verification_code = models.CharField(max_length=6, blank=True, null=True)  # SMS 인증 코드
    point1 = models.IntegerField(blank=True, null=True)
    point2 = models.IntegerField(
        blank=True,
        null=True,
        validators=[MaxValueValidator(960)]  # 상한값 10000으로 제한
    )
    
    
    def __str__(self):
        return self.user.username

# 자유게시판
class Post(models.Model):
    CATEGORY_CHOICES = [
        ('free', '자유'),
        ('info', '정보'),
        ('proposal', '제안'),
    ]
    
    postname = models.CharField(max_length=50)
    mainphoto = models.ImageField(blank=True, null=True)
    contents = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='free')
    
    # 조회수, 좋아요(숫자)
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    
    # (중요) 좋아요한 사용자 목록
    # => like 모델을 통해 연결 (through='Like')
    liked_users = models.ManyToManyField(
        User,
        blank=True,
        related_name='like_user_set',
        through='Like'
    )

    def __str__(self):
        return f"[{self.get_category_display()}] {self.postname}"
    
# 실제 중개 모델
# 위에서 through='Like' 로 지정했으면, 클래스명도 'Like'로 통일
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # 중복 좋아요 방지(UniqueConstraint)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_post_like')
        ]

    def __str__(self):
        return f"{self.user} likes {self.post}"    

class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # 유저별 1번만 기록
    
# 댓글
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.content}"
    
class infoPost(models.Model):
    postname = models.CharField(max_length=50)
    mainphoto = models.ImageField(blank=True, null=True)
    contents = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.postname