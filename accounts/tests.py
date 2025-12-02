from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Profile


class SignupTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_signup_creates_user_and_profile(self):
        resp = self.client.post(reverse("accounts_api:signup"), {"email": "a@example.com", "password": "pass1234"})
        self.assertEqual(resp.status_code, 201)
        user = User.objects.get(email="a@example.com")
        self.assertTrue(user.check_password("pass1234"))
        self.assertIsNotNone(Profile.objects.filter(user=user).first())

    def test_password_hashing(self):
        user = User.objects.create_user(username="bob", password="secret123")
        self.assertTrue(user.check_password("secret123"))
        self.assertFalse(user.check_password("wrong"))
