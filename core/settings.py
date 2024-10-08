from pathlib import Path

from decouple import config

from .jazzmin import *


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config("SECRET_KEY", cast=str, default="naruto_uzumaki")
DEBUG = config("DEBUG", cast=bool, default=True)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=str, default="*").split(", ")

DOCKER_STARTUP = config("DOCKER_STARTUP", cast=bool, default=False)
WEB_URL = config('WEB_URL', cast=str)


MY_APPS = [
    'apps.account',
    'apps.classroom',
    'apps.progress',
    'apps.education',
    'apps.bot'
]

THIRD_PARTY_APPS = [
    "phonenumber_field"
]

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
] + MY_APPS + THIRD_PARTY_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    'apps.bot.middlewares.DisableCsrfForAdmin', # off csrf check
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "core.urls"


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


WSGI_APPLICATION = "core.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql",
#             "NAME": config("POSTGRES_DB", cast=str),
#             "USER": config("POSTGRES_USER", cast=str),
#             "PASSWORD": config("POSTGRES_PASSWORD", cast=str),
#             "HOST": config("POSTGRES_HOST", cast=str),
#             "PORT": config("POSTGRES_PORT"),
#         }
#     }


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


LANGUAGE_CODE = "ru"
TIME_ZONE = "Asia/Bishkek"

USE_I18N = True
USE_TZ = True


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


X_FRAME_OPTIONS = "SAMEORIGIN"
CSP_FRAME_ANCESTORS = ("'self'", "127.0.0.1", "localhost")
CSP_DEFAULT_SRC = ("'self'", "127.0.0.1", "localhost")


TIME_INPUT_FORMATS = ['%H:%M']
