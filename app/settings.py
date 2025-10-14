from pathlib import Path
from datetime import timedelta
import os

from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# === Django básico ===
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-unsafe")
DEBUG = os.getenv("DJANGO_DEBUG", "0") == "1"

ALLOWED_HOSTS = os.getenv(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1,0.0.0.0"
).split(",")

# Confiar em origens para CSRF (útil quando acessa via porta/host diferentes ou proxy)
CSRF_TRUSTED_ORIGINS = os.getenv(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    "http://localhost,http://127.0.0.1,http://0.0.0.0"
).split(",")

# === Apps instalados ===
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # 3rd party
    "rest_framework",
    "django_filters",
    "drf_spectacular",      # OpenAPI/Swagger
    "corsheaders",          # CORS

    # Apps do projeto
    "catalog",
    "orders",
]

# === Middlewares ===
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # CORS deve vir antes de CommonMiddleware
    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"

# === Banco de dados (Postgres por padrão, SQLite opcional) ===
required_env = ["DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT"]
missing = [k for k in required_env if not os.getenv(k)]

# Permite fallback para SQLite quando explicitamente solicitado ou quando as
# variáveis de ambiente para Postgres estão ausentes (útil em desenvolvimento
# local e durante os testes automatizados).
use_sqlite_env = os.getenv("DJANGO_USE_SQLITE")
use_sqlite = (
    (use_sqlite_env == "1")
    if use_sqlite_env is not None
    else bool(missing)
)

if missing and not use_sqlite:
    raise RuntimeError(
        "Variáveis ausentes para Postgres: " + ", ".join(missing)
        + ". Defina-as no .env ou habilite DJANGO_USE_SQLITE para fallback."
    )

if use_sqlite or missing:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT", "5432"),
            "CONN_MAX_AGE": 60,
        }
    }

# === Senhas (desativado em dev) ===
AUTH_PASSWORD_VALIDATORS = []

# === Locale/Timezone ===
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# === Static & Media ===
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# === Cache (memória local; em prod use Redis) ===
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "catalog-orders-cache",
    }
}

# === CORS ===
# Em dev é prático liberar tudo; em prod prefira CORS_ALLOWED_ORIGINS
CORS_ALLOW_ALL_ORIGINS = os.getenv("CORS_ALLOW_ALL_ORIGINS", "1" if DEBUG else "0") == "1"
CORS_ALLOWED_ORIGINS = (
    [] if CORS_ALLOW_ALL_ORIGINS else os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
)

# === DRF ===
REST_FRAMEWORK = {
    # Auth
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),

    # Filtros / Busca / Ordenação
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],

    # Paginação
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,

    # OpenAPI (drf-spectacular)
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",

    # Rate limiting (throttling) básico
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "60/minute",
        "user": "300/minute",
    },
}

# === JWT ===
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# === drf-spectacular (documentação) ===
SPECTACULAR_SETTINGS = {
    "TITLE": "Catálogo & Pedidos API",
    "DESCRIPTION": "Documentação da API (OpenAPI 3) para o serviço de Catálogo e Pedidos.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# === Logging (simples e útil em dev) ===
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django.request": {"level": "WARNING", "handlers": ["console"], "propagate": False},
        "catalog": {"level": "INFO", "handlers": ["console"]},
        "orders": {"level": "INFO", "handlers": ["console"]},
    },
}
