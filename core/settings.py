import os
from pathlib import Path
import platform
import loguru
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6*qyx5x6o!f5&l#m9(qk(u4#n!k6t3^d@)xavi01y-lz^#_c-e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG')

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', 
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    #apps
    'integration.apps.IntegrationConfig',
    
    #3rd part apps
    "crispy_forms",
    "crispy_bootstrap5", 
    "debug_toolbar",
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

MYSQL_DB_NAME = config("MYSQL_DB_NAME")
MYSQL_DB_USER = config("MYSQL_DB_USER")
MYSQL_DB_PASSWORD = config("MYSQL_DB_PASSWORD")
MYSQL_DB_HOST = config("MYSQL_DB_HOST")
MYSQL_DB_PORT = config("MYSQL_DB_PORT")
USE_MYSQL = config("USE_MYSQL", cast=bool)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql" if USE_MYSQL else "django.db.backends.sqlite3",
        "NAME": MYSQL_DB_NAME if USE_MYSQL else BASE_DIR / "db.sqlite3",
        "USER": MYSQL_DB_USER if USE_MYSQL else None,
        "PASSWORD": MYSQL_DB_PASSWORD if USE_MYSQL else None,
        "HOST": MYSQL_DB_HOST if USE_MYSQL else None,
        "PORT": MYSQL_DB_PORT if USE_MYSQL else None,
        # "OPTIONS": {"charset": "utf8mb4_general_ci", "use_unicode": True},
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

USE_L10N = True

USE_THOUSAND_SEPARATOR = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [BASE_DIR / "static"]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_REDIRECT_URL = 'dashboard'
ACCOUNT_LOGOUT_REDIRECT = "login"

# Emails
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend" if DEBUG == True else "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
Email_USE_SSL=False
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

ADMINS = [
    ("Mukundi", "victormandalasijunior@gmail.com"),

]
DEFAULT_SYSTEM_USER_EMAIL = "dev@oacey.com"
DEFAULT_RECIPIENT = config('DEFAULT_RECIPIENT')
path_separator = "\\" if platform.system() == "Windows" else "/"
ASN_FILE_DESTINATION = os.path.join(BASE_DIR, f"media{path_separator}asn{path_separator}")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
TEST_FILE_STORAGE = os.path.join(BASE_DIR, f"test-data{path_separator}results.xlsx")

STATUS_CHOICES = (('Success', 'Success'), ('Failed', 'Failed'),('Pending', 'Pending'), ('Rejected', 'Rejected'))

LOGGER = loguru.logger

INTERNAL_IPS = [
    '127.0.0.1',
]
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
}

SITE_ID = 1


SESSION_EXPIRE_AT_BROWSER_CLOSE = True