from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("places/", views.places, name="places"),
    path("products/", views.products, name="products"),
    path("saved/", views.saved, name="saved"),
    path("journal/", views.journal_page, name="journal"),
    path("blog/", views.blog, name="blog"),
    path("help/", views.help_center, name="help"),
    path("contact/", views.contact, name="contact"),
    path("signin/", views.sign_in, name="signin"),
    path("signup/", views.sign_up, name="signup_page"),
    path("get-started/", views.get_started, name="get_started"),
    path("catbot/", views.catbot, name="catbot"),
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/shops/", include("shops.urls")),
    path("api/reviews/", include("reviews.urls")),
    path("api/journal/", include("journal.urls")),
    path("api/recommendations/", include("recommendations.urls")),
]
