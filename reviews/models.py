from django.db import models
from django.contrib.auth.models import User
from shops.models import CoffeeShop

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    shop = models.ForeignKey(CoffeeShop, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField()               # 1..5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    shop = models.ForeignKey(CoffeeShop, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("user","shop")
