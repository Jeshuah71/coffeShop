from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import Optional
from .models import CoffeeShop


class LocationService(ABC):
    """Abstract location provider."""

    @abstractmethod
    def get_distance_km(self, shop: CoffeeShop, user_lat: float, user_lon: float) -> Optional[float]:
        """Return approximate distance in kilometers."""


class GoogleMapsAdapter(LocationService):
    """
    Adapter around a hypothetical Google Maps client.
    Uses haversine math locally but shaped to wrap a real client.
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    def get_distance_km(self, shop: CoffeeShop, user_lat: float, user_lon: float) -> Optional[float]:
        if shop.lat is None or shop.lon is None or user_lat is None or user_lon is None:
            return None
        return round(_haversine_km(user_lat, user_lon, shop.lat, shop.lon), 2)


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371
    p = math.pi / 180
    dlat = (lat2 - lat1) * p
    dlon = (lon2 - lon1) * p
    a = 0.5 - math.cos(dlat) / 2 + math.cos(lat1 * p) * math.cos(lat2 * p) * (1 - math.cos(dlon)) / 2
    return 2 * r * math.asin(math.sqrt(a))
