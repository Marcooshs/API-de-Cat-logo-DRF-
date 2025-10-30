from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv

# === Base dir ===
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega sempre o .env (usado no Docker/CI)
load_dotenv(BASE_DIR / ".env")

# Detecta se está rodando no Docker
RUNNING_IN_DOCKER = os.getenv("RUNNING_IN_DOCKER") == "1" or Path("/.dockerenv").exists()

# Em ambiente local (fora do Docker), permite sobrescrever com .env.local
if not RUNNING_IN_DOCKER:
    load_dotenv(BASE_DIR / ".env.local", override=True)

# ---- Helpers de env ----
def env_bool(name: str, default: bool = False) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "t", "yes", "y", "on"}

def env_list(name: str, default: str = "") -> list[str]:
    raw = os.getenv(name, default)
    return [item for item in (x.strip() for x in raw.split(",")) if item]

# === Django básico ===
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-unsafe")
DEBUG = env_bool("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = env_list(
    "DJANGO_ALLOWED_HOSTS",
    default="localhost,127.0.0.1,0.0.0.0",
)

CSRF_TRUSTED_ORIGINS = env_list(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    default="http://localhost,http://127.0.0.1,http://0.0.0.0",
)

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
    "drf_spectacular",
    "corsheaders",

    # Apps do projeto
    "catalog",
    "orders",
]

# === Middlewares ===
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
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

# Fallback opcional para SQLite (útil em dev/testes)
use_sqlite_env = os.getenv("DJANGO_USE_SQLITE")
use_sqlite = (
    (use_sqlite_env == "1")
    if use_sqlite_env is not None
    else bool(missing)
)

if missing and not use_sqlite:
    raise RuntimeError(
        "Variáveis ausentes para Postgres: " + ", ".join(missing)
        + ". Defina-as no .env/.env.local ou habilite DJANGO_USE_SQLITE=1 para fallback."
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
            # No Docker: DB_HOST=db / DB_PORT=5432 (defina isso no .env usado pelo compose)
            # Fora do Docker: pode usar 127.0.0.1:5434 no .env.local, se quiser
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
CORS_ALLOW_ALL_ORIGINS = env_bool("CORS_ALLOW_ALL_ORIGINS", default=DEBUG)
CORS_ALLOWED_ORIGINS = [] if CORS_ALLOW_ALL_ORIGINS else env_list("CORS_ALLOWED_ORIGINS", default="")

# === DRF ===
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
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
