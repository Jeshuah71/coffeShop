from django.db import models
from django.utils import timezone
import secrets
from datetime import timedelta
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Simple user profile to store preferences and activity stats.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    favorite_flavors = models.JSONField(default=list, blank=True)
    preferred_drink = models.CharField(max_length=120, blank=True)
    journal_count = models.IntegerField(default=0)
    favorite_count = models.IntegerField(default=0)
    avatar_url = models.URLField(blank=True)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"Profile for {self.user.username}"

    def increment_journal(self) -> None:
        self.journal_count = (self.journal_count or 0) + 1
        self.save(update_fields=["journal_count"])

    def increment_favorite(self) -> None:
        self.favorite_count = (self.favorite_count or 0) + 1
        self.save(update_fields=["favorite_count"])


class EmailVerificationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="email_verification")
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    @staticmethod
    def new_token() -> str:
        return secrets.token_urlsafe(32)

    @classmethod
    def create_for_user(cls, user, ttl_hours: int = 48):
        token = cls.new_token()
        expires_at = timezone.now() + timedelta(hours=ttl_hours)
        obj, _ = cls.objects.update_or_create(
            user=user,
            defaults={"token": token, "expires_at": expires_at},
        )
        return obj

    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at
