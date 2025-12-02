from django.urls import path
from .views import signup, login_view, logout_view, me, profile

app_name = "accounts_api"

urlpatterns = [
    path("signup", signup, name="signup"),
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("me", me, name="me"),
    path("profile", profile, name="profile"),
]
