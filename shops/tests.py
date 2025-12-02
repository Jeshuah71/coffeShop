from django.test import TestCase
from .models import CoffeeShop


class CoffeeShopRatingTests(TestCase):
    def test_update_rating_accumulates(self):
        shop = CoffeeShop.objects.create(name="Test", avg_rating=0, rating_count=0)
        shop.update_rating(4)
        self.assertEqual(shop.avg_rating, 4)
        self.assertEqual(shop.rating_count, 1)
        shop.update_rating(2)
        self.assertAlmostEqual(shop.avg_rating, 3.0)
        self.assertEqual(shop.rating_count, 2)
