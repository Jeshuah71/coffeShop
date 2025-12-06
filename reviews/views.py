from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render
from .models import Review, Favorite
from .serializers import ReviewSerializer, FavoriteSerializer
from shops.models import CoffeeShop
from accounts.models import Profile


def home(request):
    return render(request, "home.html")


@api_view(["GET"])
def list_reviews(request):
    shop_id = request.GET.get("shopId")
    qs = Review.objects.all()
    if shop_id: 
        qs = qs.filter(shop_id=shop_id)
    return Response(ReviewSerializer(qs.order_by("-created_at")[:100], many=True).data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_review(request):
    ser = ReviewSerializer(data=request.data)
    if ser.is_valid():
        review = ser.save(user=request.user)
        try:
            review.shop.update_rating(review.rating)
        except CoffeeShop.DoesNotExist:
            pass
        return Response(ser.data, status=201)
    return Response(ser.errors, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_favorites(request):
    qs = Favorite.objects.filter(user=request.user)
    return Response(FavoriteSerializer(qs, many=True).data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_favorite(request):
    payload = request.data
    shop = None
    shop_id = payload.get("shop")
    if shop_id:
        try:
            shop = CoffeeShop.objects.get(pk=int(shop_id))
        except (CoffeeShop.DoesNotExist, ValueError, TypeError):
            shop = None

    if shop is None:
        name = (payload.get("name") or "").strip()
        if not name:
            return Response({"detail": "shop id or name required"}, status=400)
        address = (payload.get("address") or "").strip()
        lat = payload.get("lat")
        lon = payload.get("lng") or payload.get("lon")
        tags = payload.get("tags") or []
        try:
            lat = float(lat) if lat not in (None, "") else None
        except (ValueError, TypeError):
            lat = None
        try:
            lon = float(lon) if lon not in (None, "") else None
        except (ValueError, TypeError):
            lon = None
        shop = CoffeeShop.objects.create(
            name=name,
            address=address,
            lat=lat,
            lon=lon,
            tags=tags if isinstance(tags, list) else [],
        )

    fav, created = Favorite.objects.get_or_create(
        user=request.user,
        shop=shop,
    )
    if created:
        Profile.objects.get_or_create(user=request.user)[0].increment_favorite()
    return Response(
        FavoriteSerializer(fav).data,
        status=201 if created else 200
    )

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_favorite(request, shop_id:int):
    Favorite.objects.filter(user=request.user, shop_id=shop_id).delete()
    return Response(status=204)
