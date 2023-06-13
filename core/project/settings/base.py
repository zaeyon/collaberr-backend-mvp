# flake8: noqa
SECRET_KEY = NotImplemented

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
   
    # Collaberr apps
    "core.apps.accounts.apps.AccountsConfig",
    "core.apps.campaigns.apps.CampaignsConfig",
    "core.apps.home.apps.HomeConfig",

    # Third party apps
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "core/db.sqlite3",  # type: ignore
    }
}
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [(BASE_DIR / "core/templates")],  # type: ignore
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

WSGI_APPLICATION = "core.project.wsgi.application"

AUTH_USER_MODEL = "accounts.Account"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        # Implement this later
        # "OPTIONS": {"min_length": 8},
        
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    # Implement this later
    # {
    #     "NAME": "core.general.validators.PasswordValidator",
    # },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
      'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

STATIC_ROOT = "/static/"
STATICFILES_DIRS = ((BASE_DIR / "core/static"),)  # type: ignore

MEDIA_ROOT = BASE_DIR / "core/media"  # type: ignore
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# URLS
LOGIN_REDIRECT_URL = "/"
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
ROOT_URLCONF = "core.project.urls"
