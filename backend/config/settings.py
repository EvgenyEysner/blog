import sys
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# To make apps are findable without a prefix
sys.path.append(str(BASE_DIR / "apps"))

# Test testing flag
IS_TESTING = False
if "test" in sys.argv or "test_coverage" in sys.argv:
    IS_TESTING = True

env = environ.Env(
    # django
    DJANGO_DEBUG=(bool, False),
    DJANGO_USE_DEBUG_TOOLBAR=(bool, False),
    DJANGO_SECRET_KEY=(str, ""),
    DJANGO_ALLOWED_HOSTS=(list, ["127.0.0.1", "localhost", "0.0.0.0"]),
    DJANGO_DATABASE_URL=(str, "sqlite:///data.db"),
    DJANGO_SERVER_URL=(str, "http://localhost:8000"),
    DJANGO_FRONTEND_URL=(str, "http://localhost:3000"),
    DJANGO_STATIC_ROOT=(str, "staticfiles"),
    DJANGO_MEDIA_ROOT=(str, "media"),
    DJANGO_EMAIL_BACKEND=(str, "django.core.mail.backends.smtp.EmailBackend"),
    DJANGO_EMAIL_URL=(environ.Env.email_url_config, "consolemail://"),
    DJANGO_DEFAULT_FROM_EMAIL=(str, "test@test.com"),
    # Database
    DATABASE_HOST=(str, ""),
    DATABASE_NAME=(str, ""),
    DATABASE_PORT=(str, ""),
    DATABASE_USERNAME=(str, ""),
    DATABASE_PASSWORD=(str, ""),
    # CORS
    DJANGO_CORS_ORIGIN_WHITELIST=(
        list,
        [
            "http://0.0.0.0:8000",
            "http://localhost:8000",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
    ),
    DJANGO_COOKIE_DOMAIN=(str, "localhost"),
    # CSRF
    DJANGO_CSRF_COOKIE_HTTPONLY=(bool, False),
    DJANGO_SESSION_COOKIE_SAMESITE=(str, None),
    DJANGO_SESSION_COOKIE_SECURE=(bool, True),
    DJANGO_CSRF_TRUSTED_ORIGINS=(
        list,
        [
            "0.0.0.0:8000",
            "localhost:8000",
            "localhost:3000",
            "127.0.0.1:3000",
            "127.0.0.1:8000",
        ],
    ),
    # Celery
    DJANGO_CELERY_BROKER_URL=(str, ""),
    DJANGO_CELERY_TASK_ALWAYS_EAGER=(bool, False),
)

# read default env variables
environ.Env.read_env()

DEBUG = env.bool("DJANGO_DEBUG")

AUTH_USER_MODEL = "account.user"

BASE_URL = env("DJANGO_SERVER_URL")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

SITE_ID = 1

# Application definition
DJANGO_APPS = (
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "taggit",
)

THIRD_PARTY_APPS = (
    "django_db_logger",
    "django_extensions",
    # 'corsheaders',
    # 'rest_framework',
)

# add our Apps here
LOCAL_APPS = ("account", "blog")

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USERNAME"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "HOST": env("DATABASE_HOST"),
        "PORT": env("DATABASE_PORT"),
    }
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # 'corsheaders.middleware.CorsMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # AxesMiddleware should be the last middleware in the MIDDLEWARE list.
    # 'axes.middleware.AxesMiddleware',
    # To turn on per-request language requests
    # 'django.middleware.locale.LocaleMiddleware',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

MEDIA_ROOT = env("DJANGO_MEDIA_ROOT")
MEDIA_URL = "/media/"

STATIC_URL = "/static/"
STATIC_ROOT = env("DJANGO_STATIC_ROOT")

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

STATICFILES_DIRS = ("static",)

ROOT_URLCONF = "config.urls"

FRONTEND_URL = env("DJANGO_FRONTEND_URL")

# CORS
# CORS_ORIGIN_WHITELIST = env.list('DJANGO_CORS_ORIGIN_WHITELIST')
# CORS_ALLOWED_ORIGINS = (f'{FRONTEND_URL}',)
# CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_METHODS = default_methods

# CSRF
# store csrf token in cookie instead of the session to make it possible
# see ajax howto in django docs: https://docs.djangoproject.com/en/3.2/ref/csrf/#ajax
# CSRF_USE_SESSIONS = False
# CSRF_FAILURE_VIEW = 'account.views.csrf_failure'
# CSRF_TRUSTED_ORIGINS = env.list('DJANGO_CSRF_TRUSTED_ORIGINS')
# CSRF_COOKIE_HTTPONLY = env.bool('DJANGO_CSRF_COOKIE_HTTPONLY')
# CSRF_COOKIE_SECURE = env.bool('DJANGO_SESSION_COOKIE_SECURE')
# CSRF_COOKIE_SAMESITE = env.str('DJANGO_SESSION_COOKIE_SAMESITE')

# SESSION_COOKIE_SAMESITE = env.str('DJANGO_SESSION_COOKIE_SAMESITE')
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SESSION_COOKIE_AGE = 1209600  # 2 weeks
# SESSION_COOKIE_SECURE = env.bool('DJANGO_SESSION_COOKIE_SECURE')
# SESSION_COOKIE_HTTPONLY = env.bool('DJANGO_CSRF_COOKIE_HTTPONLY')

# CSRF_COOKIE_DOMAIN = env.str('DJANGO_COOKIE_DOMAIN')
# SESSION_COOKIE_DOMAIN = env.str('DJANGO_COOKIE_DOMAIN')

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
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

# Password validation + custom password validation
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
    {
        "NAME": "account.password_validation.EntirelyAlphabeticPasswordValidator",
    },
    {
        "NAME": "account.password_validation.EntirelyNonCapitalLetterPasswordValidator",
    },
    {
        "NAME": "account.password_validation.NoSmallLetterPasswordValidator",
    },
    {
        "NAME": "account.password_validation.EntirelyNoneSpecialCharactersPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

# The Language Code is purposely chosen as english ('en') otherwise the we can't guarantee that a user with a non
# supported language (not German nor English) gets the english content by default. To see the backend in German the
# browser must have German selected as the main language the 'django.middleware.locale.LocaleMiddleware' makes sure
# to see the backend in the language one has selected in the browser.
LANGUAGE_CODE = "de-De"

TIME_ZONE = "Europe/Berlin"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

# Starting with 3.2 new projects are generated with DEFAULT_AUTO_FIELD set to BigAutoField
# We set it back to AutoField for compatibility reasons with external libraries, e.g.
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Logging
DB_LOGGER_ENTRY_LIFETIME = 30
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "db_handler": {
            "level": "DEBUG",
            "class": "django_db_logger.db_log_handler.DatabaseLogHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "default": {
            "level": "DEBUG",
            "handlers": ["console", "db_handler"],
            "propagate": True,
        }
    },
}

# the following code should be always at the end of this file
if IS_TESTING:
    DEBUG = False
    PYTHONUNBUFFERED = 0

    LOGGING["loggers"]["default"]["level"] = "WARNING"
    LOGGING["loggers"]["default"]["handlers"] = ["console"]

# Celery settings
CELERY_TIMEZONE = "Europe/Berlin"
CELERY_BROKER_URL = env("DJANGO_CELERY_BROKER_URL")
CELERY_TASK_ALWAYS_EAGER = env("DJANGO_CELERY_TASK_ALWAYS_EAGER")

CELERY_RESULT_BACKEND = "rpc://"
CELERY_TASK_CREATE_MISSING_QUEUES = True
CELERY_RETRY_DELAY = 15
CELERY_RETRY_MAX_TIMES = 15  # 15 retries

# Email server configuration
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = True
