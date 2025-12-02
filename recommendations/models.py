from django.db import models


class Quote(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=120, blank=True)
    mood_tag = models.CharField(max_length=50, default="neutral")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.mood_tag}: {self.text[:40]}"
