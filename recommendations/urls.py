from django.urls import path
from . import views

urlpatterns = [
    # POST /api/recommendations/ to get ranked shops based on prompt text
    path("", views.recommend, name="recommend"),
    path("catbot", views.catbot, name="catbot"),
]
