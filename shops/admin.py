from django.contrib import admin
from .models import CoffeeShop, MenuItem


@admin.register(CoffeeShop)
class CoffeeShopAdmin(admin.ModelAdmin):
    list_display = ("name", "avg_rating", "rating_count", "price_level")
    search_fields = ("name", "address")
    list_filter = ("price_level",)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "shop", "category", "price", "seasonal")
    search_fields = ("name", "shop__name")
    list_filter = ("seasonal", "category")
