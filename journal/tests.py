from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from shops.models import CoffeeShop
from journal.models import JournalEntry


class JournalEntryTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="alice", password="pass1234")
        self.client.force_authenticate(self.user)
        self.shop = CoffeeShop.objects.create(name="Journal Cafe")

    def test_create_and_list_journal_entry(self):
        resp = self.client.post(reverse("journal_create"), {
            "shop": self.shop.id,
            "visit_date": "2024-01-01",
            "my_rating": 4,
            "notes": "Nice vibes"
        }, format="json")
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(JournalEntry.objects.filter(user=self.user).count(), 1)

        list_resp = self.client.get(reverse("journal_list"))
        self.assertEqual(list_resp.status_code, 200)
        self.assertEqual(len(list_resp.json()), 1)
