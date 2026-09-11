"""
Django settings for EduMail Generator project.

Generated on 2026-09-11
"""

import os
from pathlib import Path
from decouple import config

# বেস ডিরেক্টরি
BASE_DIR = Path(__file__).resolve().parent.parent

# সিক্রেট কী
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production-mode')

# ডিবাগ মোড
DEBUG = config('DEBUG', default=True, cast=bool)

# অনুমোদিত হোস্ট
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# ইনস্টল করা অ্যাপ্লিকেশন
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # তৃতীয় পক্ষ অ্যাপ
    'rest_framework',
    'corsheaders',
    
    # আমাদের অ্যাপ
    'users.apps.UsersConfig',
    'institutions.apps.InstitutionsConfig',
    'students.apps.StudentsConfig',
    'emails.apps.EmailsConfig',
    'core.apps.CoreConfig',
]

# মিডলওয়্যার
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# রুট URL কনফিগারেশন
ROOT_URLCONF = 'config.urls'

# টেমপ্লেট কনফিগারেশন
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# WSGI অ্যাপ্লিকেশন
WSGI_APPLICATION = 'config.wsgi.application'

# ডাটাবেস কনফিগারেশন
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': config('DATABASE_NAME', default='edumail_generator'),
        'USER': config('DATABASE_USER', default='edumail_user'),
        'PASSWORD': config('DATABASE_PASSWORD', default='password'),
        'HOST': config('DATABASE_HOST', default='localhost'),
        'PORT': config('DATABASE_PORT', default='5432'),
    }
}

# পাসওয়ার্ড যাচাইকরণ
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

# আন্তর্জাতিকীকরণ
LANGUAGE_CODE = 'bn-bd'
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_TZ = True

# স্ট্যাটিক ফাইল
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# মিডিয়া ফাইল
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ডিফল্ট প্রাইমারি কী ধরন
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# কাস্টম ইউজার মডেল
AUTH_USER_MODEL = 'users.CustomUser'

# সেশন সেটিংস
SESSION_COOKIE_AGE = 1209600  # ২ সপ্তাহ
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
SESSION_COOKIE_HTTPONLY = True

# CSRF সেটিংস
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)
CSRF_COOKIE_HTTPONLY = True
CSRF_TRUSTED_ORIGINS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# SSL রিডাইরেক্ট
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)

# ইমেইল সেটিংস (SendGrid)
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
SENDGRID_API_KEY = config('SENDGRID_API_KEY', default='')
SENDGRID_FROM_EMAIL = config('SENDGRID_FROM_EMAIL', default='noreply@edumail-generator.com')

# লগিং কনফিগারেশন
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# REST Framework কনফিগারেশন
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# CORS সেটিংস
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
]

CORS_ALLOW_CREDENTIALS = True
