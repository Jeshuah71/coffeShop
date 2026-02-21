from django.urls import path
from .views import signup, login_view, logout_view, me, profile, resend_verification, verify_email

app_name = "accounts_api"

urlpatterns = [
    path("signup", signup, name="signup"),
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("me", me, name="me"),
    path("profile", profile, name="profile"),
    path("resend", resend_verification, name="resend"),
    path("verify", verify_email, name="verify"),
]
