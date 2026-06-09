from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.shortcuts import redirect
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
import os
import requests
from .models import Profile, EmailVerificationToken
from .serializers import ProfileSerializer, UserSerializer

def _app_base_url(request) -> str:
    base = os.getenv("APP_BASE_URL", "").strip()
    if base:
        return base.rstrip("/")
    return request.build_absolute_uri("/").rstrip("/")

def _send_verification_email(user: User, token_obj: EmailVerificationToken, request) -> bool:
    api_key = os.getenv("RESEND_API_KEY", "").strip()
    from_email = os.getenv("RESEND_FROM_EMAIL", "").strip()
    if not api_key or not from_email:
        if settings.DEBUG:
            verify_url = f"{_app_base_url(request)}/api/auth/verify?token={token_obj.token}"
            print("\nDEV EMAIL VERIFICATION LINK:")
            print(verify_url)
            print()
            return True
        return False
    verify_url = f"{_app_base_url(request)}/api/auth/verify?token={token_obj.token}"
    subject = "Verify your Coffee Corner account"
    html = f"""
    <div style="font-family:Arial,sans-serif;line-height:1.5;">
      <h2>Verify your Coffee Corner account</h2>
      <p>Thanks for signing up! Click the button below to verify your email address.</p>
      <p><a href="{verify_url}" style="display:inline-block;padding:10px 16px;background:#d46b42;color:#fff;border-radius:999px;text-decoration:none;">Verify email</a></p>
      <p>If the button doesn’t work, paste this link into your browser:</p>
      <p><a href="{verify_url}">{verify_url}</a></p>
    </div>
    """
    resp = requests.post(
        "https://api.resend.com/emails",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "from": from_email,
            "to": [user.email],
            "subject": subject,
            "html": html,
        },
        timeout=10,
    )
    return resp.status_code < 300

@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    email = request.data.get("email"); password = request.data.get("password")
    if not email or not password:
        return Response({"detail":"email and password required"}, status=400)
    existing = User.objects.filter(email=email).first()
    if existing:
        if not existing.is_active:
            token_obj = EmailVerificationToken.create_for_user(existing)
            _send_verification_email(existing, token_obj, request)
            return Response({"detail":"verification email sent"}, status=200)
        return Response({"detail":"email already registered"}, status=400)
    username = request.data.get("username") or email.split("@")[0]
    avatar = request.data.get("avatar_url") or ""
    if User.objects.filter(username=username).exists():
        return Response({"detail":"username taken"}, status=400)
    with transaction.atomic():
        user = User.objects.create_user(username=username, email=email, password=password, is_active=False)
        prof, _ = Profile.objects.get_or_create(user=user)
        if avatar:
            prof.avatar_url = avatar
            prof.save(update_fields=["avatar_url"])
        token_obj = EmailVerificationToken.create_for_user(user)
        sent = _send_verification_email(user, token_obj, request)
    if not sent:
        return Response({"detail":"verification email could not be sent"}, status=500)
    return Response({"detail":"verification email sent"}, status=201)

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    u = request.data.get("username") or request.data.get("email")
    pwd = request.data.get("password")
    if not u or not pwd: return Response({"detail":"username/email and password required"}, status=400)
    if "@" in u:
        pending = User.objects.filter(email=u).first()
        if pending and not pending.is_active:
            return Response({"detail":"Please verify your email before signing in."}, status=403)
    if "@" in u:
        try: u = User.objects.get(email=u).username
        except User.DoesNotExist: pass
    user = authenticate(request, username=u, password=pwd)
    if not user: return Response({"detail":"invalid credentials"}, status=400)
    login(request, user)
    return Response({"id":user.id,"username":user.username,"email":user.email})

@api_view(["POST"])
def logout_view(request):
    logout(request); return Response({"detail":"logged out"})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    u = request.user
    return Response(UserSerializer(u).data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):
    prof, _ = Profile.objects.get_or_create(user=request.user)
    return Response(ProfileSerializer(prof).data)

@api_view(["POST"])
@permission_classes([AllowAny])
def resend_verification(request):
    email = request.data.get("email")
    if not email:
        return Response({"detail":"email required"}, status=400)
    user = User.objects.filter(email=email).first()
    if not user:
        return Response({"detail":"email not found"}, status=404)
    if user.is_active:
        return Response({"detail":"already verified"}, status=400)
    token_obj = EmailVerificationToken.create_for_user(user)
    sent = _send_verification_email(user, token_obj, request)
    if not sent:
        return Response({"detail":"verification email could not be sent"}, status=500)
    return Response({"detail":"verification email sent"}, status=200)

@api_view(["GET"])
@permission_classes([AllowAny])
def verify_email(request):
    token = request.query_params.get("token")
    if not token:
        return redirect("/signin?verify=invalid")
    token_obj = EmailVerificationToken.objects.filter(token=token).first()
    if not token_obj or token_obj.is_expired():
        return redirect("/signin?verify=expired")
    user = token_obj.user
    user.is_active = True
    user.save(update_fields=["is_active"])
    token_obj.delete()
    return redirect("/signin?verify=success")
