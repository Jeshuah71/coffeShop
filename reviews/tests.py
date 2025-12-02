from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Review, Favorite
from shops.models import CoffeeShop
from accounts.models import Profile


class ReviewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="eve", password="pass1234")
        self.client.force_authenticate(self.user)
        self.shop = CoffeeShop.objects.create(name="Test Cafe")

    def test_create_review(self):
        self.assertEqual(Review.objects.count(), 0)
        resp = self.client.post(reverse("reviews:reviews_create"), {"shop": self.shop.id, "rating": 5}, format="json")
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Review.objects.count(), 1)

    def test_list_reviews(self):
        Review.objects.create(user=self.user, shop=self.shop, rating=4)
        resp = self.client.get(reverse("reviews:reviews_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)

    def test_requires_auth_for_create(self):
        client = APIClient()
        resp = client.post(reverse("reviews:reviews_create"), {"shop": self.shop.id, "rating": 5})
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(Review.objects.count(), 0)


class FavoriteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="favuser", password="pass1234")
        self.client.force_authenticate(self.user)
        self.shop = CoffeeShop.objects.create(name="Fav Cafe")

    def test_add_and_list_favorite(self):
        add_resp = self.client.post(reverse("reviews:reviews_add_favorite"), {"shop": self.shop.id}, format="json")
        self.assertIn(add_resp.status_code, (200, 201))
        self.assertEqual(Favorite.objects.filter(user=self.user, shop=self.shop).count(), 1)
        list_resp = self.client.get(reverse("reviews:reviews_list_favorites"))
        self.assertEqual(list_resp.status_code, 200)
        self.assertEqual(len(list_resp.json()), 1)

    def test_remove_favorite(self):
        Favorite.objects.create(user=self.user, shop=self.shop)
        del_resp = self.client.delete(reverse("reviews:reviews_remove_favorite", args=[self.shop.id]))
        self.assertEqual(del_resp.status_code, 204)
        self.assertEqual(Favorite.objects.filter(user=self.user, shop=self.shop).count(), 0)

    def test_requires_auth(self):
        client = APIClient()
        resp = client.post(reverse("reviews:reviews_add_favorite"), {"shop": self.shop.id}, format="json")
        self.assertEqual(resp.status_code, 403)
