from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Post

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(pre_save, sender=Post)
def set_default_status_for_bug(sender, instance, **kwargs):
    # 버그제보 카테고리인 경우 기본값을 'in_progress'로 설정
    if instance.category == 'bug' and not instance.status:
        instance.status = 'in_progress'