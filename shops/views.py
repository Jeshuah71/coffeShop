from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import CoffeeShop, MenuItem
from .serializers import CoffeeShopSerializer, MenuItemSerializer

@api_view(["GET"])
def list_shops(request):
    q = request.GET.get("query","").strip()
    tags = request.GET.getlist("tags")
    qs = CoffeeShop.objects.all()
    if q:
        qs = qs.filter(Q(name__icontains=q)|Q(address__icontains=q)|Q(tags__icontains=q))
    for t in tags: qs = qs.filter(tags__icontains=t)
    return Response(CoffeeShopSerializer(qs.order_by("-avg_rating")[:100], many=True).data)

@api_view(["GET"])
def shop_detail(request, pk:int):
    try: shop = CoffeeShop.objects.get(pk=pk)
    except CoffeeShop.DoesNotExist: return Response({"detail":"not found"}, status=404)
    return Response(CoffeeShopSerializer(shop).data)

@api_view(["GET"])
def shop_menu(request, pk:int):
    items = MenuItem.objects.filter(shop_id=pk)
    return Response(MenuItemSerializer(items, many=True).data)
