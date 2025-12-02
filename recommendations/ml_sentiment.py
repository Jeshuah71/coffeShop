from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


class SentimentAnalyzer:
    """
    Toy sentiment/mood classifier for journal entry text.
    Implements a simple Singleton via get_instance.
    """

    _instance = None

    @classmethod
    def get_instance(cls) -> "SentimentAnalyzer":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._initialized = True
        self.vectorizer = TfidfVectorizer()
        self.model = LogisticRegression()
        self._train()

    def _train(self) -> None:
        texts = [
            "I had an amazing latte, feeling energized and happy",
            "So tired and stressed, coffee didn't help much",
            "Relaxed afternoon in a cozy cafe",
            "Rushed visit, long line, frustrating",
        ]
        labels = ["happy", "tired", "calm", "stressed"]
        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)

    def predict_mood(self, text: str) -> str:
        if not text.strip():
            return "neutral"
        X = self.vectorizer.transform([text])
        return self.model.predict(X)[0]
