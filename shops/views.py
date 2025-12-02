from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import CoffeeShop, MenuItem
from .serializers import CoffeeShopSerializer, MenuItemSerializer
from .services import GoogleMapsAdapter

@api_view(["GET"])
def list_shops(request):
    q = request.GET.get("query","").strip()
    tags = request.GET.getlist("tags")
    user_lat = request.GET.get("lat"); user_lon = request.GET.get("lon")
    qs = CoffeeShop.objects.all()
    if q:
        qs = qs.filter(Q(name__icontains=q)|Q(address__icontains=q)|Q(tags__icontains=q))
    for t in tags: qs = qs.filter(tags__icontains=t)
    adapter = GoogleMapsAdapter()
    shops = []
    for shop in qs.order_by("-avg_rating")[:100]:
        shop.distance_km = None
        if user_lat and user_lon:
            try:
                shop.distance_km = adapter.get_distance_km(shop, float(user_lat), float(user_lon))
            except ValueError:
                shop.distance_km = None
        shops.append(shop)
    return Response(CoffeeShopSerializer(shops, many=True).data)

@api_view(["GET"])
def shop_detail(request, pk:int):
    try: shop = CoffeeShop.objects.get(pk=pk)
    except CoffeeShop.DoesNotExist: return Response({"detail":"not found"}, status=404)
    return Response(CoffeeShopSerializer(shop).data)

@api_view(["GET"])
def shop_menu(request, pk:int):
    items = MenuItem.objects.filter(shop_id=pk)
    return Response(MenuItemSerializer(items, many=True).data)
