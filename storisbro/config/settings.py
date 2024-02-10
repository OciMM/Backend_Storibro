"""
Django settings for storisbro project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Для связи с фронтендом
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000'
]

CORS_ALLOW_CREDENTIALS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'social_django',
    'django_extensions',
    'corsheaders',
    'drf_spectacular',

    'authentication.apps.AuthenticationConfig',
    'confirmation.apps.ConfirmationConfig',
    'notification.apps.NotificationConfig',
    'ref.apps.RefConfig',
    'commission.apps.CommissionConfig',
    'communities.apps.CommunitiesConfig',
    'creatives.apps.CreativesConfig',
    'download_video.apps.DownloadVideoConfig',
    'reservation.apps.ReservationConfig',
    'content.apps.ContentConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'Storisbro_back_db',
        'USER': 'storisbro_back_login',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': 5432
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

# добавил
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend',
                           'social_core.backends.vk.VKOAuth2',
]

AUTHENTICATION_METHOD = 'email'

CSRF_COOKIE_SECURE = False


# Настройки vk
SOCIAL_AUTH_VK_OAUTH2_KEY = 'djtwQXn7cSwsj6ccaf0j'
SOCIAL_AUTH_VK_OAUTH2_SECRET = '4e96d4d44e96d4d44e96d4d49b4d81deec44e964e96d4d42b24bccff014114d6cd3f1cc'
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']
LOGIN_URL = 'localhost'
LOGIN_REDIRECT_URL = 'https://vk.com/feed'

SOCIAL_AUTH_URL_NAMESPACE = 'authentication:social'


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    
    
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Время жизни access token
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),  # Время жизни refresh token
    'SLIDING_TOKEN_LIFETIME': timedelta(days=7),  # Время жизни sliding token
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=14),  # Время жизни refresh sliding token
    'AUTH_HEADER_TYPES': ('Bearer',),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Network API",
    "DESCRIPTION": "Awesome network API",
    'VERSION': "1.0.0",
    "SCHEMA": {
        "swagger": "2.0",
    },
}

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'bekasovmaks20@gmail.com'  # Замените на свой адрес электронной почты Gmail
EMAIL_HOST_PASSWORD = 'jhwy sfwp efkj qdjz'  # Укажите пароль от вашего Gmail аккаунта
EMAIL_USE_TLS = True

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


AUTH_USER_MODEL = 'authentication.User'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Moscow'

CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'DEBUG',
    },
}