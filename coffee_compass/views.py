from django.conf import settings
from django.contrib.auth import logout
from django.core.exceptions import FieldError
from django.db.models import Q, Avg
from django.shortcuts import redirect, render

from shops.models import CoffeeShop


def home(request):
    return render(
        request,
        "home.html",
        {"google_maps_api_key": getattr(settings, "GOOGLE_MAPS_API_KEY", "")},
    )


def places(request):
    """
    Server-rendered places finder with simple filters.
    Filters:
      - city: case-insensitive contains match on city/address.
      - q: partial match on name or address.
      - radius (miles): filters on distance_miles if the field exists (falls back to km if present).
      - open_now: filters on boolean open_now if present; otherwise skips this filter.
    """
    city = (request.GET.get("city") or "").strip()
    query = (request.GET.get("q") or "").strip()
    radius_raw = request.GET.get("radius")
    if radius_raw is None:
        radius_raw = request.GET.get("miles")
    if radius_raw is None:
        radius_raw = "10"

    radius = radius_raw
    radius_val: float | None
    if radius_raw == "":
        radius_val = None
    else:
        try:
            radius_val = float(radius_raw)
        except (TypeError, ValueError):
            radius_val = 10.0
            radius = "10"
    open_now = "open_now" in request.GET

    qs = CoffeeShop.objects.all()

    # Filter by city if possible (fall back to address).
    if city:
        try:
            qs = qs.filter(city__icontains=city)
        except FieldError:
            qs = qs.filter(address__icontains=city)

    # Filter by name/address keyword.
    if query:
        qs = qs.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query)
        )

    # Filter by distance if a distance field exists.
    field_names = {f.name for f in CoffeeShop._meta.get_fields()}
    if radius_val is not None and radius_val > 0:
        if "distance_miles" in field_names:
            qs = qs.filter(distance_miles__lte=radius_val)
        elif "distance_km" in field_names:
            qs = qs.filter(distance_km__lte=radius_val * 1.60934)

    # Filter by open_now if the field exists; otherwise skip.
    if open_now and "open_now" in field_names:
        qs = qs.filter(open_now=True)

    qs = qs.annotate(journal_rating=Avg("journal_entries__my_rating"))
    shops = list(qs[:100])

    def to_miles(shop):
        if hasattr(shop, "distance_miles") and shop.distance_miles is not None:
            return round(float(shop.distance_miles), 1)
        if hasattr(shop, "distance_km") and shop.distance_km is not None:
            return round(float(shop.distance_km) * 0.621371, 1)
        return None

    shops_json = []
    for s in shops:
        distance_val = to_miles(s)
        # Attach a transient attribute for template readability.
        setattr(s, "distance_display", distance_val)
        if not hasattr(s, "open_now"):
            setattr(s, "open_now", None)
        rating = getattr(s, "journal_rating", None) or getattr(s, "avg_rating", None)
        shops_json.append(
            {
                "name": s.name,
                "address": getattr(s, "address", ""),
                "lat": getattr(s, "lat", None),
                "lng": getattr(s, "lon", None),
                "distance_miles": distance_val,
                "open_now": getattr(s, "open_now", None),
                "rating": float(rating) if rating is not None else None,
                "tags": getattr(s, "tags", []) or [],
                "id": s.id,
            }
        )

    context = {
        "google_maps_api_key": getattr(settings, "GOOGLE_MAPS_API_KEY", ""),
        "shops": shops,
        "filters": {"city": city, "q": query, "radius": radius, "open_now": open_now},
        "shops_json": json.dumps(shops_json),
    }
    return render(request, "pages/places.html", context)


def products(request):
    return render(request, "pages/products.html")


def saved(request):
    return render(request, "pages/saved.html")


def blog(request):
    return render(request, "pages/blog.html")

def journal_page(request):
    rating_slots = list(range(5))  # 5 stars, half steps handled in JS
    return render(
        request,
        "pages/journal.html",
        {"rating_slots": rating_slots},
    )


def help_center(request):
    return render(request, "pages/help.html")


def contact(request):
    return render(request, "pages/contact.html")


def sign_in(request):
    return render(request, "pages/signin.html")

def sign_up(request):
    return render(request, "pages/signup.html")

def get_started(request):
    return render(request, "pages/get_started.html")

def logout_redirect(request):
    """
    Session logout helper that works with a GET from the navbar and then
    returns the user to the home page.
    """
    if request.user.is_authenticated:
        logout(request)
    return redirect("home")


def catbot(request):
    return render(request, "pages/catbot.html")
import json
