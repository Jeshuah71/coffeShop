from rest_framework import serializers
from .models import JournalEntry
from shops.models import CoffeeShop

class JournalEntrySerializer(serializers.ModelSerializer):
    shop_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = JournalEntry
        fields = ["id","user","shop","item","visit_date","my_rating","notes","created_at","shop_name"]
        read_only_fields = ["user","created_at","shop_name"]
        extra_kwargs = {
            "item": {"required": False, "allow_null": True},
        }

    def get_shop_name(self, obj):
        try:
            return obj.shop.name
        except CoffeeShop.DoesNotExist:
            return None
