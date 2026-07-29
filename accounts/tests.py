from datetime import timedelta

from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
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
        self.assertFalse(user.is_active)
        self.assertIsNotNone(Profile.objects.filter(user=user).first())

    def test_password_hashing(self):
        user = User.objects.create_user(username="bob", password="secret123")
        self.assertTrue(user.check_password("secret123"))
        self.assertFalse(user.check_password("wrong"))


class ProfileEmailVerificationTests(TestCase):
    def test_is_email_verified_is_false_without_timestamp(self):
        user = User.objects.create_user(username="pending")
        profile = Profile.objects.create(user=user)

        self.assertFalse(profile.is_email_verified)

    def test_is_email_verified_is_true_with_timestamp(self):
        user = User.objects.create_user(username="verified")
        profile = Profile.objects.create(
            user=user,
            email_verified_at=timezone.now(),
        )

        self.assertTrue(profile.is_email_verified)


class EmailVerificationStateMigrationTests(TransactionTestCase):
    migrate_from = ("accounts", "0003_merge_20260527_1554")
    migrate_to = ("accounts", "0004_profile_email_verified_at")

    def setUp(self):
        super().setUp()
        self.executor = MigrationExecutor(connection)
        self.executor.migrate([self.migrate_from])
        self.old_apps = self.executor.loader.project_state(
            [self.migrate_from]
        ).apps

    def tearDown(self):
        self.executor.loader.build_graph()
        self.executor.migrate(self.executor.loader.graph.leaf_nodes())
        super().tearDown()

    def test_migration_separates_verification_from_is_active(self):
        User = self.old_apps.get_model("auth", "User")
        Profile = self.old_apps.get_model("accounts", "Profile")
        EmailVerificationToken = self.old_apps.get_model(
            "accounts", "EmailVerificationToken"
        )

        pending_user = User.objects.create(
            username="pending-migration",
            is_active=False,
        )
        Profile.objects.create(user=pending_user)
        EmailVerificationToken.objects.create(
            user=pending_user,
            token="pending-token",
            expires_at=timezone.now() + timedelta(hours=48),
        )

        active_user = User.objects.create(
            username="active-migration",
            is_active=True,
        )
        Profile.objects.create(user=active_user)

        disabled_user = User.objects.create(
            username="disabled-migration",
            is_active=False,
        )
        Profile.objects.create(user=disabled_user)

        self.executor = MigrationExecutor(connection)
        self.executor.migrate([self.migrate_to])
        new_apps = self.executor.loader.project_state([self.migrate_to]).apps
        User = new_apps.get_model("auth", "User")
        Profile = new_apps.get_model("accounts", "Profile")

        pending_user = User.objects.get(pk=pending_user.pk)
        pending_profile = Profile.objects.get(user_id=pending_user.pk)
        active_user = User.objects.get(pk=active_user.pk)
        active_profile = Profile.objects.get(user_id=active_user.pk)
        disabled_user = User.objects.get(pk=disabled_user.pk)
        disabled_profile = Profile.objects.get(user_id=disabled_user.pk)

        self.assertTrue(pending_user.is_active)
        self.assertIsNone(pending_profile.email_verified_at)
        self.assertTrue(active_user.is_active)
        self.assertIsNotNone(active_profile.email_verified_at)
        self.assertFalse(disabled_user.is_active)
        self.assertIsNotNone(disabled_profile.email_verified_at)
