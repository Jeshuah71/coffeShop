from django.urls import path
from .views import list_shops, shop_detail, shop_menu

urlpatterns = [
    path("", list_shops, name = "list_shops"),                 # GET /api/shops
    path("<int:pk>", shop_detail, name = "shop_detail"),        # GET /api/shops/:id
    path("<int:pk>/menu", shop_menu, name = "shop_menu"),     # GET /api/shops/:id/menu
]
