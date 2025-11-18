from django.contrib import admin
from django.urls import path, include
from reviews.views import home

urlpatterns = [
    
    
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/shops/", include("shops.urls")),
    path("api/reviews/", include("reviews.urls")),
    path("api/journal/", include("journal.urls")),
    path("api/recommendations/", include("recommendations.urls")),
]
