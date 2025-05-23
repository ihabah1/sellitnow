﻿import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Load environment variables from .env
load_dotenv()


# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: Keep this secret in production!
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")

# SECURITY WARNING: Don't run with debug=True in production!
DEBUG = os.getenv("DEBUG", "True") == "True"


# Allowed hosts
#ALLOWED_HOSTS = ["sellitnow-production.up.railway.app", "127.0.0.1", "localhost","34.205.255.124"]
ALLOWED_HOSTS = ["*"]


CSRF_TRUSTED_ORIGINS = [
    "https://sellitnow-production.up.railway.app",
]

# Application definition
INSTALLED_APPS = [
    "admin_interface",
    "colorfield",  # Dependency for admin-interface
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app",  # Your custom app
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # ✅ Ensure this is here!
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "sellitnow.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "app/templates"],  # Template directory
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",  # Required for allauth
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "sellitnow.wsgi.application"

USE_LOCAL_DB = os.environ.get('USE_LOCAL_DB', 'True') == 'True'

if USE_LOCAL_DB:
    try:
        # Attempt to connect to the local DB to ensure it's available
        conn = psycopg2.connect(
            dbname='django_app',
            user='postgres',
            password='  ',  # double spaces
            host='localhost',
            port='5432',
        )
        conn.close()
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'django_app',
                'USER': 'postgres',
                'PASSWORD': '  ',
                'HOST': 'localhost',
                'PORT': '5432',
            }
        }
    except Exception as e:
        print(f"Local DB connection failed, falling back to cloud DB. Error: {e}")
        DATABASES = {
            'default': dj_database_url.config(
                default='postgresql://postgres:hSEjZdGIqLGMoYOtbIYLPxbNxwQrtKFc@interchange.proxy.rlwy.net:50440/railway',
                conn_max_age=600,
                ssl_require=True,
            )
        }
else:
    DATABASES = {
        'default': dj_database_url.config(
            default='postgresql://postgres:hSEjZdGIqLGMoYOtbIYLPxbNxwQrtKFc@interchange.proxy.rlwy.net:50440/railway',
            conn_max_age=600,
            ssl_require=True,
        )
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# settings.py

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'app/static']  # Ensure this path is correct
STATIC_ROOT = BASE_DIR / 'staticfiles'

#STATIC_URL = "/static/"
#STATIC_ROOT = BASE_DIR / "staticfiles"  # This is required for collectstatic
#STATICFILES_DIRS = [BASE_DIR / "app/static"] if (BASE_DIR / "app/static").exists() else []

# Media files (Uploaded content)
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
}

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication settings
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

# Django-Allauth settings (Updated)
# ACCOUNT_LOGIN_METHODS = "email"  # Replaces ACCOUNT_AUTHENTICATION_METHOD

# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_RATE_LIMITS = {
    "login_failed": "5/m",  # 5 failed login attempts per minute
    "login": "10/m",  # 10 successful logins per minute
}

# Allow login with either username or email
ACCOUNT_LOGIN_METHODS = {'username', 'email'}

# Make username required
ACCOUNT_USERNAME_REQUIRED = True

# Keep email optional (if needed)
ACCOUNT_EMAIL_REQUIRED = False 
ACCOUNT_EMAIL_VERIFICATION = "optional"  # Adjust as needed


# Login URLs
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Email settings (Use environment variables for production security)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "sandbox.smtp.mailtrap.io")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "5618690533dd66")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "72a7bccc645082")
EMAIL_PORT = os.getenv("EMAIL_PORT", "2525")
DEFAULT_FROM_EMAIL = "no-reply@yourdomain.com"

# Enable Whitenoise for static file management (Optional)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Cloudinary settings for media files
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
}

# Customizing session settings (Optional)
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_NAME = "sessionid"
