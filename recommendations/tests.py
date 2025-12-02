from django.test import TestCase
from django.contrib.auth.models import User
from recommendations.ml_sentiment import SentimentAnalyzer
from recommendations.agent import CatChatbotAgent
from recommendations.services import QuoteRecommender
from recommendations.models import Quote
from journal.models import JournalEntry
from shops.models import CoffeeShop
from django.utils import timezone


class SentimentAnalyzerTests(TestCase):
    def test_predict_mood(self):
        analyzer = SentimentAnalyzer.get_instance()
        self.assertEqual(analyzer.predict_mood("Relaxed afternoon with a cozy cappuccino"), "calm")
        self.assertEqual(analyzer.predict_mood("Rushed visit, long line, frustrating"), "stressed")


class CatChatbotTests(TestCase):
    def test_catbot_responses(self):
        agent = CatChatbotAgent()
        self.assertIn("explore", agent.get_response("how do i use coffee compass").lower())
        self.assertIn("Meow", agent.get_response(""))


class QuoteRecommenderTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="quote", password="pass1234")
        self.shop = CoffeeShop.objects.create(name="Quote Shop")
        Quote.objects.create(text="Calm quote", mood_tag="calm")
        Quote.objects.create(text="Happy quote", mood_tag="happy")

    def test_quote_recommender_returns_quote(self):
        JournalEntry.objects.create(
            user=self.user,
            shop=self.shop,
            visit_date=timezone.now().date(),
            my_rating=4,
            notes="Relaxed afternoon in a cozy cafe"
        )
        qr = QuoteRecommender()
        quote = qr.get_daily_quote_for_user(self.user)
        self.assertIsNotNone(quote)


class ObserverTests(TestCase):
    def test_observer_notify(self):
        from recommendations.observer import HomeFeedSubject, FeedObserver

        class DummyObserver(FeedObserver):
            def __init__(self):
                self.updated = False
            def update(self, user):
                self.updated = True

        subject = HomeFeedSubject()
        obs = DummyObserver()
        subject.attach(obs)
        subject.notify(None)
        self.assertTrue(obs.updated)
