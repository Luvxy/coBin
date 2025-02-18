from .models import Post
import math

def postlist_processor(request):
    base_height = 60  # 기본 텍스트 높이 (px)
    image_height = 0  # 이미지 포함 시 추가 높이 (px)
    max_height_vh = 60  # CSS 기준 높이 (60vh)
    viewport_height = request.GET.get("viewport_height", 900)  # JS에서 전달한 높이 (기본 900px)
    max_height = math.floor((int(viewport_height) * max_height_vh) / 100)  # px 변환

    current_height = 0
    selected_posts = []

    posts = Post.objects.all().order_by('-id')

    for post in posts:
        has_image = hasattr(post, 'image') and post.mainphoto  # 이미지 필드 확인
        total_height = base_height + (image_height if has_image else 0)

        if current_height + total_height > max_height:
            break  # 최대 높이 초과하면 중단

        selected_posts.append(post)
        current_height += total_height

    return {'postlist': selected_posts}
