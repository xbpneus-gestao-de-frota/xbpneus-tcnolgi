from pathlib import Path
import os
import dj_database_url
from decouple import config
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)


def _split_env_list(value):
    """Split comma-separated environment values into a clean Python list."""
    if not value:
        return []
    if isinstance(value, (list, tuple)):
        return [item for item in value if item]
    return [item.strip() for item in str(value).split(",") if item.strip()]


ALLOWED_HOSTS = _split_env_list(config("ALLOWED_HOSTS", default=""))
if not ALLOWED_HOSTS:
    if DEBUG:
        ALLOWED_HOSTS = ["*"]
    else:
        raise RuntimeError("ALLOWED_HOSTS must be defined when DEBUG is False.")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "rest_framework_simplejwt",
    "corsheaders",
    "backend.transportador",
    "backend.motorista",
    "backend.borracharia",
    "backend.revenda",
    "backend.recapagem",
    "backend.common",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "backend.core.middleware.RoleMiddleware", # Adicionado RoleMiddleware
]

ROOT_URLCONF = "backend.core.urls"

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

WSGI_APPLICATION = "backend.core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL")
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Django 4.2+ usa a configuração STORAGES para definir as backends padrão.
# Mantemos o armazenamento local para uploads (default) e habilitamos o
# ManifestStaticFilesStorage do WhiteNoise para garantir que os assets sejam
# versionados corretamente em produção.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Garantimos que os finders padrão estejam ativos para que collectstatic localize
# tanto arquivos dentro dos apps quanto em diretórios estáticos adicionais.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Quando os arquivos estáticos não foram coletados ainda (por exemplo, em builds
# falhos), permitir o fallback impede 500 no Admin, mantendo o endpoint disponível
# para troubleshooting até que o pipeline seja corrigido.
WHITENOISE_MANIFEST_STRICT = False

if DEBUG:
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_AUTOREFRESH = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

_cors_allowed_origins = _split_env_list(config("CORS_ALLOWED_ORIGINS", default=""))

if _cors_allowed_origins:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = _cors_allowed_origins
else:
    CORS_ALLOW_ALL_ORIGINS = config(
        "CORS_ALLOW_ALL_ORIGINS", default=DEBUG, cast=bool
    )
    if CORS_ALLOW_ALL_ORIGINS:
        CORS_ALLOWED_ORIGINS = []
    elif DEBUG:
        CORS_ALLOWED_ORIGINS = []
    else:
        raise RuntimeError(
            "CORS_ALLOWED_ORIGINS must be set or CORS_ALLOW_ALL_ORIGINS enabled when DEBUG is False."
        )

# Configuração JWT
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'USER_AUTHENTICATION_RULE': 'backend.common.custom_auth.CustomUserAuthenticationRule',
}

