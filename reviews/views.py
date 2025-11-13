from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render   # ⬅️ ADD THIS
from .models import Review, Favorite
from .serializers import ReviewSerializer, FavoriteSerializer


def home(request):                     # ⬅️ ADD THIS
    return render(request, "reviews/home.html")


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
        ser.save(user=request.user)
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
    ser = FavoriteSerializer(data={"shop": request.data.get("shop")})
    if ser.is_valid():
        fav, created = Favorite.objects.get_or_create(
            user=request.user, 
            shop=ser.validated_data["shop"]
        )
        return Response(
            FavoriteSerializer(fav).data, 
            status=201 if created else 200
        )
    return Response(ser.errors, status=400)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_favorite(request, shop_id:int):
    Favorite.objects.filter(user=request.user, shop_id=shop_id).delete()
    return Response(status=204)
