from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "testpass"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

    def test_login(self):
        # Test that user can login
        url = reverse("login")
        data = {"username": self.username, "password": self.password}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    def test_logout(self):
        # Test that user can logout
        url = reverse("logout")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
