from django.urls import path
from .views import list_reviews, create_review, list_favorites, add_favorite, remove_favorite

app_name = "reviews"

urlpatterns = [
    path("", list_reviews, name="reviews_list"),
    path("create", create_review, name="reviews_create"),
    path("favorites", list_favorites, name="reviews_list_favorites"),
    path("favorites/add", add_favorite, name="reviews_add_favorite"),
    path("favorites/<int:shop_id>", remove_favorite, name="reviews_remove_favorite"),
]
