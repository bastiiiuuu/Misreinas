

"""Configuración local por defecto y requisitos explícitos para una publicación HTTPS."""

import os
import secrets
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = [host.strip() for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost,[::1]").split(",") if host.strip()]
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# La clave local persiste entre reinicios para conservar sesiones, pero no se versiona.
# En producción se exige una clave independiente y no se genera un valor de respaldo.
if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured("Define DJANGO_SECRET_KEY para ejecutar con DJANGO_DEBUG=0.")
    key_file = BASE_DIR / ".local-secret"
    try:
        with key_file.open("x", encoding="utf-8") as stream:
            stream.write(secrets.token_urlsafe(50))
    except FileExistsError:
        pass
    SECRET_KEY = key_file.read_text(encoding="utf-8").strip()

if not DEBUG and (len(SECRET_KEY) < 50 or SECRET_KEY.startswith("django-insecure-")):
    raise ImproperlyConfigured("La clave de producción debe ser aleatoria, privada y tener al menos 50 caracteres.")

SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = not DEBUG
STATIC_ROOT = BASE_DIR / "staticfiles"


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core.apps.CoreConfig",
    "ofertas.apps.OfertasConfig",
    "categorias.apps.CategoriasConfig",
    "about.apps.AboutConfig",
    "contact.apps.ContactConfig",
    "sucursales.apps.SucursalesConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "core.middleware.Pagina404Middleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "misreinas.urls"

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

WSGI_APPLICATION = "misreinas.wsgi.application"
ASGI_APPLICATION = "misreinas.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Permite comprobar una instalación limpia sin abrir la base de trabajo.
DATABASES['default']['NAME'] = Path(os.environ.get('DJANGO_DB_PATH', BASE_DIR / 'db.sqlite3'))
