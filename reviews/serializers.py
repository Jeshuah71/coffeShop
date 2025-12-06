from rest_framework import serializers
from .models import Review, Favorite
from shops.serializers import CoffeeShopSerializer

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id","user","shop","rating","comment","created_at"]
        read_only_fields = ["user","created_at"]

class FavoriteSerializer(serializers.ModelSerializer):
    shop_detail = CoffeeShopSerializer(source="shop", read_only=True)
    class Meta:
        model = Favorite
        fields = ["id","user","shop","shop_detail","created_at"]
        read_only_fields = ["user","created_at"]
