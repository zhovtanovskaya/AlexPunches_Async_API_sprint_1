import os
from pathlib import Path

import sentry_sdk
from dotenv import load_dotenv
from sentry_sdk.integrations.django import DjangoIntegration
from split_settings.tools import include

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

include(
    'components/database.py',
    'components/apps.py',
    'components/middleware.py',
    'components/templates.py',
    'components/validators.py',
    'components/logger.py',
)

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', False) == 'True'
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', '127.0.0.1:8000', '127.0.0.1:8000']
ROOT_URLCONF = 'example.urls'
WSGI_APPLICATION = 'example.wsgi.application'

CORS_ALLOWED_ORIGINS = ['http://127.0.0.1:8080', 'http://localhost:8080', 'http://127.0.0.1:8000', 'http://localhost:8000']
LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000']

SHELL_PLUS = "ipython"

sentry_sdk.init(
    dsn=os.environ.get('ADMIN_SENTRY_DNS'),
    integrations=[
        DjangoIntegration(),
    ],
    traces_sample_rate=1.0,
    send_default_pii=True
)
