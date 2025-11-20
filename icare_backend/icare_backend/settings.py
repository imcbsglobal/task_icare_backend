"""
Django settings for icare_backend project.
"""

from pathlib import Path
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
# -----------------------------
# Base Directory
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# Security
# -----------------------------
SECRET_KEY = 'django-insecure-0t@zpkf9!^%&ok8mhrrm5vh9r%pf&#@m#g^iv!_4)=!4w0dp=!'
DEBUG = True
ALLOWED_HOSTS = ['*','www.icare.imcbs.com','icare.imcbs.com']

# -----------------------------
# Installed Apps
# -----------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',

    # Local App
    'icare_app',

    # Third-party Apps
    'rest_framework',
    'corsheaders',
]

# -----------------------------
# Middleware
# -----------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -----------------------------
# URL and WSGI Configuration
# -----------------------------
ROOT_URLCONF = 'icare_backend.urls'
WSGI_APPLICATION = 'icare_backend.wsgi.application'

# -----------------------------
# Templates
# -----------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# -----------------------------
# Database
# -----------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'task_icare_db',
        'USER': 'postgres',
        'PASSWORD': 'info@imc',
        'HOST': '88.222.212.14',
        'PORT': '5432',
    }
}

# -----------------------------
# Password Validation
# -----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -----------------------------
# Internationalization
# -----------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# -----------------------------
# Static Files
# -----------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# -----------------------------
# Media Files
# -----------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Cloudflare R2 Storage Configuration
CLOUDFLARE_R2_ENABLED = os.getenv('CLOUDFLARE_R2_ENABLED', 'false').lower() == 'true'

if CLOUDFLARE_R2_ENABLED:
    # R2 Credentials
    AWS_ACCESS_KEY_ID = os.getenv('CLOUDFLARE_R2_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = os.getenv('CLOUDFLARE_R2_SECRET_KEY')
    
    # R2 Configuration
    CLOUDFLARE_R2_BUCKET_NAME = os.getenv('CLOUDFLARE_R2_BUCKET')
    CLOUDFLARE_R2_ENDPOINT = os.getenv('CLOUDFLARE_R2_BUCKET_ENDPOINT')
    CLOUDFLARE_R2_PUBLIC_URL = os.getenv('CLOUDFLARE_R2_PUBLIC_URL')
    CLOUDFLARE_R2_ACCOUNT_ID = os.getenv('CLOUDFLARE_R2_ACCOUNT_ID', '')

    
    # Django 5.x STORAGES setting (replaces DEFAULT_FILE_STORAGE)
    STORAGES = {
        "default": {
            "BACKEND": "icare_backend.storage_backends.R2MediaStorage",

        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
    
    # Media files URL
    if CLOUDFLARE_R2_PUBLIC_URL:
        MEDIA_URL = f'{CLOUDFLARE_R2_PUBLIC_URL}/media/'
        # STATIC_URL = f'{CLOUDFLARE_R2_PUBLIC_URL}/static/'
    else:
        MEDIA_URL = f'{CLOUDFLARE_R2_ENDPOINT}/{CLOUDFLARE_R2_BUCKET_NAME}/media/'
else:
    # Local storage fallback
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
    MEDIA_URL = '/media/'




# ----------------------------
# Default Primary Key Field Type
# -----------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -----------------------------
# Django REST Framework
# -----------------------------
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
}

# -----------------------------
# CORS / CSRF Settings
# -----------------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",  
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "https://icare.imcbs.com"
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False

SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = False

# -----------------------------
# Session Settings (for Login Tracking)
# -----------------------------
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 24 hours in seconds
SESSION_SAVE_EVERY_REQUEST = True
