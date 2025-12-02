from django.db import models
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

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"Profile for {self.user.username}"

    def increment_journal(self) -> None:
        self.journal_count = (self.journal_count or 0) + 1
        self.save(update_fields=["journal_count"])

    def increment_favorite(self) -> None:
        self.favorite_count = (self.favorite_count or 0) + 1
        self.save(update_fields=["favorite_count"])
