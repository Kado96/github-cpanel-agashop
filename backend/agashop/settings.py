from pathlib import Path
from datetime import timedelta
import sys
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-default-change-me')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# Liste des hôtes autorisés (définie dans .env ou par défaut local)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',') + [
    "api.agashop.bi",
    "agashop.bi",
    "www.agashop.bi",
    "www.api.agashop.bi", 
]

# CORS Configuration pour développement local
# Permet toutes les origines en développement (localhost, 127.0.0.1, etc.)
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Application definition
sys.path.insert(0, str(BASE_DIR / 'api'))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',  # Pour la blacklist des tokens JWT
    'api.accounts',
    'api.shops',
]

MIDDLEWARE = [
    # CORS doit être en PREMIER pour fonctionner correctement
    'corsheaders.middleware.CorsMiddleware',
    
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'api.middlewares.DisableCSRF',
    'api.middlewares.ExceptionMiddleware',
]

ROOT_URLCONF = 'agashop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'agashop.wsgi.application'


# Database
# En local : SQLite par défaut. En production (Render/Supabase) : surcharge via DATABASE_URL ou paramètres POSTGRES
import dj_database_url

DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DB_HOST = config('DB_HOST', default=None)
    if DB_HOST:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': config('DB_NAME', default='postgres'),
                'USER': config('DB_USER', default='postgres'),
                'PASSWORD': config('DB_PASSWORD', default=''),
                'HOST': DB_HOST,
                'PORT': config('DB_PORT', default='5432'),
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    BASE_DIR / "static"
]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'PAGE_SIZE_QUERY_PARAM': 'page_size',
    'MAX_PAGE_SIZE': 100000,
    'PAGINATE_BY_PARAM': 'limit'
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=3),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=6),
}



# ==========================
# EMAIL CONFIGURATION (CPANEL - agashop.bi)
# ==========================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = os.getenv("EMAIL_HOST", "mail.agashop.bi")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "agashop@agashop.bi")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

EMAIL_USE_SSL = True
EMAIL_USE_TLS = False

DEFAULT_FROM_EMAIL = f"Agashop <{EMAIL_HOST_USER}>"

EMAIL_TIMEOUT = 20
    
# ==========================
# STORAGE SDK CONFIGURATION (SUPABASE S3 / GOOGLE DRIVE / LOCAL)
# ==========================
STORAGE_PROVIDER = config('STORAGE_PROVIDER', default='SUPABASE_S3')
LOCAL_STORAGE_BASE_PATH = config('LOCAL_STORAGE_BASE_PATH', default=os.path.join(MEDIA_ROOT, 'sdk_storage'))
GOOGLE_APPLICATION_CREDENTIALS = config('GOOGLE_APPLICATION_CREDENTIALS', default='')
GOOGLE_DRIVE_SHARED_DRIVE_ID = config('GOOGLE_DRIVE_SHARED_DRIVE_ID', default='')

SUPABASE_S3_ENDPOINT_URL = config('SUPABASE_S3_ENDPOINT_URL', default='https://plihtjkucujoeewlzptb.storage.supabase.co/storage/v1/s3')
SUPABASE_S3_ACCESS_KEY_ID = config('SUPABASE_S3_ACCESS_KEY_ID', default='')
SUPABASE_S3_SECRET_ACCESS_KEY = config('SUPABASE_S3_SECRET_ACCESS_KEY', default='')
SUPABASE_S3_BUCKET_NAME = config('SUPABASE_S3_BUCKET_NAME', default='media')
SUPABASE_S3_REGION_NAME = config('SUPABASE_S3_REGION_NAME', default='eu-west-1')

