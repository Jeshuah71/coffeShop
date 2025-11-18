from pathlib import Path
import os

# Optional: load .env if present
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Core ---
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-not-secret")
DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,web").split(",") if h.strip()]

# --- Apps ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "accounts",
    "shops",
    "reviews",
    "journal",
    "recommendations",
]

# --- Middleware ---
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "coffee_compass.urls"
WSGI_APPLICATION = "coffee_compass.wsgi.application"
ASGI_APPLICATION = "coffee_compass.asgi.application"

# --- Templates ---
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# --- I18N / Static ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Denver"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- DRF / CORS ---
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.SessionAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
}
CORS_ALLOW_ALL_ORIGINS = True  # dev

# --- Database: force POSTGRES_* in Docker; SQLite fallback elsewhere ---
POSTGRES_HOST = (os.getenv("POSTGRES_HOST") or "").strip()
if POSTGRES_HOST:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "coffee_compass"),
            "USER": os.getenv("POSTGRES_USER", "cc_user"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "supersecret"),
            "HOST": POSTGRES_HOST,  # 'db' on docker-compose network
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Debug print (sanitized) so we SEE what Django is using at startup
if os.getenv("PRINT_DB_DEBUG", "true").lower() == "true":
    db = DATABASES["default"].copy()
    if db.get("PASSWORD"):
        db["PASSWORD"] = "******"
    print("🔧 Django DB config ->", db)
