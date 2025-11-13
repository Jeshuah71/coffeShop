from rest_framework import serializers
from .models import CoffeeShop, MenuItem

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ["id","name","category","seasonal","price","flavor_tags"]

class CoffeeShopSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True)
    class Meta:
        model = CoffeeShop
        fields = ["id","name","address","lat","lon","price_level","avg_rating","hours","tags","menu_items"]

