from datetime import datetime

from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import JournalEntry
from .serializers import JournalEntrySerializer
from shops.models import CoffeeShop
from recommendations.services import QuoteRecommender, ShopRecommender
from recommendations.observer import HomeFeedSubject, QuoteObserver, RecommendationObserver
from accounts.models import Profile

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_entries(request):
    qs = JournalEntry.objects.filter(user=request.user).order_by("-visit_date","-created_at")
    return Response(JournalEntrySerializer(qs, many=True).data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_entry(request):
    data = request.data.copy()
    # Accept a freeform place name and create/link a CoffeeShop if no shop id was provided.
    place_name = data.get("place_name") or data.get("place")
    shop_id = data.get("shop")
    if not shop_id and not place_name:
        return Response({"detail": "Place name is required."}, status=400)
    if not shop_id and place_name:
        shop, _ = CoffeeShop.objects.get_or_create(
            name=place_name.strip(),
            defaults={
                "address": data.get("address", ""),
                "lat": data.get("lat"),
                "lon": data.get("lng") or data.get("lon"),
            },
        )
        data["shop"] = str(shop.id)
    elif shop_id:
        data["shop"] = str(shop_id)

    # Remove non-model fields before validation.
    for key in ["place_name", "address", "lat", "lng", "photo"]:
        data.pop(key, None)

    # Normalize date input to ISO; fall back to today for invalid input.
    raw_date = data.get("visit_date")
    parsed_date = None
    if raw_date:
        if isinstance(raw_date, datetime):
            parsed_date = raw_date.date()
        else:
            for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m-%d-%Y", "%d/%m/%Y"):
                try:
                    parsed_date = datetime.strptime(str(raw_date), fmt).date()
                    break
                except ValueError:
                    continue
    if parsed_date is None:
        parsed_date = timezone.now().date()
    data["visit_date"] = parsed_date.isoformat()

    # Normalize rating to halves; default to 0.5 if missing
    try:
        r = float(data.get("my_rating"))
        data["my_rating"] = max(0.5, min(5.0, round(r * 2) / 2))
    except (TypeError, ValueError):
        data["my_rating"] = 0.5

    ser = JournalEntrySerializer(data=data)
    if ser.is_valid():
        entry = ser.save(user=request.user)
        Profile.objects.get_or_create(user=request.user)[0].increment_journal()
        subject = HomeFeedSubject()
        subject.attach(QuoteObserver(QuoteRecommender()))
        subject.attach(RecommendationObserver(ShopRecommender()))
        try:
            subject.notify(request.user)
        except Exception:
            # Feed updates are best-effort; journal save should still succeed.
            pass
        return Response(ser.data, status=201)
    return Response({"detail": "Invalid journal entry", "errors": ser.errors}, status=400)
