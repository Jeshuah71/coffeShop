from django.urls import path
from .views import list_reviews, create_review, list_favorites, add_favorite, remove_favorite

urlpatterns = [
    path("", list_reviews),                   # GET /api/reviews?shopId=
    path("create", create_review),            # POST /api/reviews/create
    path("favorites", list_favorites),        # GET /api/reviews/favorites
    path("favorites/add", add_favorite),      # POST {shop:id}
    path("favorites/<int:shop_id>", remove_favorite),  # DELETE
]
