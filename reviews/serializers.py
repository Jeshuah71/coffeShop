from rest_framework import serializers
from .models import Review, Favorite

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id","user","shop","rating","comment","created_at"]
        read_only_fields = ["user","created_at"]

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ["id","user","shop","created_at"]
        read_only_fields = ["user","created_at"]
