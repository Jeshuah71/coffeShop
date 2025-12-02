from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


class FeedObserver(ABC):
    @abstractmethod
    def update(self, user) -> None:
        """React to user activity changes."""


class FeedSubject(ABC):
    def __init__(self):
        self._observers: List[FeedObserver] = []

    def attach(self, observer: FeedObserver) -> None:
        self._observers.append(observer)

    def detach(self, observer: FeedObserver) -> None:
        self._observers.remove(observer)

    def notify(self, user) -> None:
        for observer in list(self._observers):
            observer.update(user)


class HomeFeedSubject(FeedSubject):
    """Subject triggered on journal entry creation."""
    pass


class QuoteObserver(FeedObserver):
    def __init__(self, quote_recommender):
        self.quote_recommender = quote_recommender
        self.cache = {}

    def update(self, user) -> None:
        quote = self.quote_recommender.get_daily_quote_for_user(user)
        if quote:
            self.cache[user.id] = quote


class RecommendationObserver(FeedObserver):
    def __init__(self, recommender):
        self.recommender = recommender
        self.cache = {}

    def update(self, user) -> None:
        items = self.recommender.recommend("cozy work spot", limit=3)
        self.cache[user.id] = items
