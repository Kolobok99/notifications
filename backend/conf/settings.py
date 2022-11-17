from loguru import logger

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", default='django-insecure-nm_h-x*1#se4anh9uf)')

DEBUG = bool(int(os.environ.get("DEBUG", default=1)))

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", default="localhost 127.0.0.1").split(" ")


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'apps.api',
    'apps.polls',
    'apps.mailings',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'conf.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE', default='django.db.backends.postgresql'),
        'NAME': os.environ.get('SQL_NAME', default='nots_db'),
        'USER': os.environ.get('SQL_USER', default='manager'),
        'PASSWORD': os.environ.get('SQL_PASSWORD', default='manager_password'),
        'HOST': os.environ.get('SQL_HOST', default='dev_db'),
        'PORT': os.environ.get('SQL_PORT', default='5432'),
    }
}

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

LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE', default='ru')

TIME_ZONE = os.environ.get('TIME_ZONE', default='Europe/Moscow')

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "docs")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "swagger_files")]


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#REDIS:
REDIS_HOST = os.environ.get('REDIS_HOST', default='0.0.0.0')
REDIS_PORT = os.environ.get('REDIS_PORT', default='6379')

#REDIS:
# REDIS_HOST = 'redis'
# REDIS_PORT = '6379'

#CELERY
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ":" + REDIS_PORT + "/0"
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ":" + REDIS_PORT + '/0'
CELERY_ACCEPT_CONTENT = {'application/json'}
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


#EMAIL
EMAIL_HOST = os.environ.get('EMAIL_HOST', default='smtp.mail.ru')
EMAIL_PORT = os.environ.get('EMAIL_PORT', default='2525')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', default='mail@mail.ru')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', default='host_pass')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', default='mail@gmail.com')


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ]

}

API_KEY = os.environ.get('API_KEY', default='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDAxMjEyOTEsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6IkBaSUFfOTg3In0.NfjBxMbrpsgv4MyX6LYhCSy0gRZNxs5m94M9eJtdRZ4')

logger.add(
    "logs/log.json",
    format="{time} - {level} - {file}  - {message}",
    level=os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
    rotation="10 MB",
    compression="zip",
    serialize=True,
)

logger.add(
    "logs/log.log",
    format="{time} - {level} - {file} - {message}",
    level=os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
    rotation="10 MB",
    compression="zip",
    serialize=False,
    backtrace=False,
    diagnose=False
)

logger.add(
    "logs/log_full_traceback.log",
    format="{time} - {level} - {file} - {module} - {message}",
    level=os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
    rotation="10 MB",
    compression="zip",
    serialize=False,
    backtrace=True,
    diagnose=True
)



