from __future__ import annotations

from typing import List
from shops.models import CoffeeShop
from shops.serializers import CoffeeShopSerializer
from .tags import text_to_tags
from .scoring import score_shop, to_reason
from .ml_sentiment import SentimentAnalyzer
from .models import Quote
from journal.models import JournalEntry
from django.utils import timezone
from datetime import timedelta


class ShopRecommender:
    """Uses tags and ratings to recommend shops."""

    def recommend(self, prompt: str, limit: int = 3) -> List[dict]:
        tagset = text_to_tags(prompt)
        shops = list(CoffeeShop.objects.all())
        scored = sorted(shops, key=lambda s: score_shop(s, tagset), reverse=True)[:limit]
        return [
            {
                "shop": CoffeeShopSerializer(s).data,
                "reason": to_reason(s, tagset),
                "score": round(score_shop(s, tagset), 3),
            }
            for s in scored
        ]


class QuoteRecommender:
    """
    Selects a 'daily quote' based on user's recent journal entries and predicted mood.
    """

    def __init__(self, analyzer: SentimentAnalyzer | None = None):
        self.analyzer = analyzer or SentimentAnalyzer.get_instance()

    def get_daily_quote_for_user(self, user) -> Quote | None:
        recent_entries = JournalEntry.objects.filter(
            user=user,
            created_at__gte=timezone.now() - timedelta(days=7),
        ).order_by("-created_at")

        if recent_entries.exists():
            combined_text = " ".join(e.notes for e in recent_entries if e.notes)
            mood = self.analyzer.predict_mood(combined_text)
            quote = Quote.objects.filter(mood_tag=mood).order_by("?").first()
            if quote:
                return quote
        return Quote.objects.order_by("?").first()
