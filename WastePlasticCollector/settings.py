"""
Django settings for WastePlasticCollector project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import dj_database_url
import os
from pathlib import Path
import datetime
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECRET_KEY = os.environ.get("SECRET_KEY")
SECRET_KEY = 'django-insecure-n&ejxsg)u00(9gz5^2&7!(e-6iavmll_@4pz2=(u7vcz%$)^v0'

# SECURITY WARNING: don't run with debug turned on in production!


# DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

# ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")
DEBUG = True

ALLOWED_HOSTS = []



REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASS': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}


# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=1),
#     'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
# }
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Example: 5 minutes
    'REFRESH_TOKEN_LIFETIME': timedelta(days=6),    # Example: 1 day
    # 'ROTATE_REFRESH_TOKENS': False,
    # 'BLACKLIST_AFTER_ROTATION': True,
    # 'UPDATE_LAST_LOGIN': False,

    # 'ALGORITHM': 'HS256',
    # 'VERIFYING_KEY': None,
    # 'AUDIENCE': None,
    # 'ISSUER': None,
    # 'JWK_URL': None,
    # 'LEEWAY': 0,

    # 'AUTH_HEADER_TYPES': ('Bearer',),
    # 'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    # 'USER_ID_FIELD': 'id',
    # 'USER_ID_CLAIM': 'user_id',
    # 'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    # 'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    # 'TOKEN_TYPE_CLAIM': 'token_type',

    # 'JTI_CLAIM': 'jti',

    # 'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    # 'SLIDING_TOKEN_LIFETIME': timedelta(minutes=6),
    # 'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(minutes=6),
}

CSRF_COOKIE_HTTPONLY = False
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000']  # Add your domain here



AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    "allauth.account.auth_backends.AuthenticationBackend"
]




# Application definition

INSTALLED_APPS = [
    "daphne",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'UserManagement',
    'WastePlasticCollectorApp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'UserManagement.middleware.JWTAuthenticationMiddleware',
]

ROOT_URLCONF = 'WastePlasticCollector.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        }
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

WSGI_APPLICATION = 'WastePlasticCollector.wsgi.application'
# 👇 4. Add the below line for asgi config
ASGI_APPLICATION = 'WastePlasticCollector.asgi.application'


# 👇 5. Add the below line for channel layer
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': "channels.layers.InMemoryChannelLayer"
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  # Your SMTP port number
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'muler3044@gmail.com'  # Sender email
EMAIL_HOST_PASSWORD = 'exswfaucprkqjcgq'  # Sender email password

# Add the URL of your frontend or where the password reset form is hosted
PASSWORD_RESET_URL = 'http://your-frontend-url/reset-password'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',

    }
}

# database_url = os.environ.get("DATABASE_URL")
# DATABASES["default"] = dj_database_url.parse(database_url)


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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (str(BASE_DIR.joinpath('static')),)
STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_PROFILE_MODULE = 'UserManagement.CustomUsers'

AUTH_USER_MODEL = 'UserManagement.CustomUsers'
AUTHENTICATION_BACKENDS = [
    'UserManagement.authentication.CustomAuthenticationBackend',
    # 'WastePlasticCollectorApp.authentication.CustomAuthenticationBackend',
]

