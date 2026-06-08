from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Post


class PostModelTests(TestCase):
    def test_bug_posts_default_to_in_progress_when_created_by_view(self):
        user = User.objects.create_user(username="author", password="pw")
        self.client.force_login(user)

        response = self.client.post(
            reverse("new_post", kwargs={"category": "bug"}),
            {"postname": "Bug report", "contents": "Something is broken."},
        )

        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(postname="Bug report")
        self.assertEqual(post.category, "bug")
        self.assertEqual(post.status, "in_progress")

    def test_in_progress_post_only_accessible_to_author_or_staff(self):
        author = User.objects.create_user(username="author", password="pw")
        other = User.objects.create_user(username="other", password="pw")
        staff = User.objects.create_user(username="staff", password="pw", is_staff=True)
        post = Post.objects.create(
            postname="Private bug",
            contents="Pending fix",
            author=author,
            category="bug",
            status="in_progress",
        )

        self.assertTrue(post.is_accessible_by(author))
        self.assertFalse(post.is_accessible_by(other))
        self.assertTrue(post.is_accessible_by(staff))


class BasicViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="viewer", password="pw")
        self.client = Client()
        self.client.force_login(self.user)

    def test_search_matches_post_title_and_content(self):
        Post.objects.create(
            postname="Strategy note",
            contents="RSI entry",
            author=self.user,
            category="strategy",
        )

        response = self.client.get(reverse("search"), {"q": "RSI"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Strategy note")

    def test_post_list_loads_category(self):
        Post.objects.create(
            postname="Free post",
            contents="Hello",
            author=self.user,
            category="free",
        )

        response = self.client.get(reverse("post_list", kwargs={"category": "free"}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Free post")
