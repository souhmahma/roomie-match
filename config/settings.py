from decouple import config
import dj_database_url
from pathlib import Path
import os
DEBUG = True
BASE_DIR = Path(__file__).resolve().parent.parent
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party
    'django_htmx',
    # Local
    'accounts',
    'listings',
    'matching',
    'messaging',
    'visits',
    'django_celery_results',



    
]

AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Pour tes templates globaux (base.html)
        'APP_DIRS': True,                 # Pour chercher dans les dossiers d'apps
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

LOGIN_URL           = '/accounts/login/'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = '/'

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL       = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
ROOT_URLCONF = 'config.urls'

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default=f"sqlite:///{BASE_DIR}/db.sqlite3"),
        conn_max_age=600 # Optionnel : garde la connexion ouverte pour plus de rapidité
    )
}

# Celery
CELERY_BROKER_URL        = config('REDIS_URL')
CELERY_RESULT_BACKEND    = config('REDIS_URL')
CELERY_ACCEPT_CONTENT    = ['json']
CELERY_TASK_SERIALIZER   = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Email
EMAIL_BACKEND       = config('EMAIL_BACKEND')
EMAIL_HOST          = config('EMAIL_HOST')
EMAIL_PORT          = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS       = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER     = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL  = config('DEFAULT_FROM_EMAIL')

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage

