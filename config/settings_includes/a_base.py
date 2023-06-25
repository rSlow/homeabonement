import sys
from pathlib import Path

from config.settings_includes.env import get_env

BASE_DIR = Path(__file__).resolve().parent.parent.parent

APPS_DIR = BASE_DIR / "apps"
sys.path.insert(0, str(APPS_DIR))

ENV_DIR = BASE_DIR / "env"
ENV = get_env(env_dir=ENV_DIR)

SECRET_KEY = ENV.str("SECRET_KEY")
DEBUG = ENV.bool("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]
ALLOWED_HOSTS.extend(ENV.list("ALLOWED_HOSTS"))

CSRF_TRUSTED_ORIGINS: list = ENV.list("DOMAIN", [])  # for ngrok
CSRF_TRUSTED_ORIGINS.extend(ENV.list("CSRF_TRUSTED_ORIGINS", []))

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.admindocs",
    # Third-party
    "allauth",
    "allauth.account",
    'captcha',
    "debug_toolbar",
    "phonenumber_field",
    "django_cleanup",
    'compressor',
    # Local
    "apps.accounts.apps.AccountsConfig",
    "apps.pages.apps.PagesConfig",
    "apps.courses.apps.CoursesConfig",
    "apps.payments.apps.PaymentsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
            APPS_DIR / "accounts" / "templates",  # allauth
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "config.context_processors.env_ctx_processor",
            ],
            'libraries': {
                'debug': 'apps.accounts.templatetags.debug',
                'user': 'apps.accounts.templatetags.user',
            },
        },
    },
]

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

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = BASE_DIR / "public_html" / "static"
STATIC_URL = "/static/"

STATICFILES_DIRS = [BASE_DIR / "static"]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

MEDIA_ROOT = BASE_DIR / "public_html" / "media"
MEDIA_URL = "/media/"

INTERNAL_IPS = ["127.0.0.1"]

AUTH_USER_MODEL = "accounts.CustomUser"

LOGIN_REDIRECT_URL = "profile"

DOMAIN = ENV.str("DOMAIN")

TIME_FORMAT = "%d-%m-%Y %H:%M:%S"
