from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Post


class BlogCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_create_post_with_valid_data(self):
        self.client.login(username="testuser", password="testpass")
        data = {"title": "Test post", "content": "This is a test post."}
        response = self.client.post(reverse("blog-create"), data)
        self.assertEqual(response.status_code, 302)  # Expect a redirect
        self.assertEqual(Post.objects.count(), 1)  # Expect one post to be created
        post = Post.objects.first()
        self.assertEqual(post.title, "Test post")
        self.assertEqual(post.content, "This is a test post.")
        self.assertEqual(post.author, self.user)

    def test_create_post_with_invalid_data(self):
        self.client.login(username="testuser", password="testpass")
        data = {"title": "", "content": ""}
        response = self.client.post(reverse("blog-create"), data)
        self.assertEqual(response.status_code, 200)  # Expect the same page to reload
        self.assertEqual(Post.objects.count(), 0)  # Expect no posts to be created


class BlogViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.post = Post.objects.create(
            title="Test post", content="This is a test post.", author=self.user
        )

    def test_view_post_with_existing_data(self):
        url = reverse("post", args=[self.post.pk, self.post.title])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Expect a successful response
        self.assertContains(
            response, "Test post"
        )  # Expect the post title to be displayed
        self.assertContains(
            response, "This is a test post."
        )  # Expect the post content to be displayed

    def test_view_post_with_nonexistent_data(self):
        url = reverse("post", args=[99, "nonexistent"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)  # Expect a 404 error
