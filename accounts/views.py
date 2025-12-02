from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer, UserSerializer

@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    email = request.data.get("email"); password = request.data.get("password")
    if not email or not password:
        return Response({"detail":"email and password required"}, status=400)
    username = request.data.get("username") or email.split("@")[0]
    if User.objects.filter(username=username).exists():
        return Response({"detail":"username taken"}, status=400)
    with transaction.atomic():
        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.get_or_create(user=user)
    return Response(UserSerializer(user).data, status=201)

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    u = request.data.get("username") or request.data.get("email")
    pwd = request.data.get("password")
    if not u or not pwd: return Response({"detail":"username/email and password required"}, status=400)
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
