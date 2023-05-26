from .base import os  # flake8: noqa: F403
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from .base import *  # noqa: F403, F401
DEBUG = False


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'SISTEMA-TIT',
        'USER': 'datic@datic-app-db',
        'PASSWORD': '6y342z0VaOQa',
        'HOST': 'datic-app-db.postgres.database.azure.com',
        'PORT': '5432',
    }
}

MEDIA_ROOT = '/media/'  # Docker volume
STATIC_ROOT = "/public/"  # Docker volume

sentry_sdk.init(
    dsn="http://d0393edd210348698c87134d0c3dc6fd@20.102.86.65:9000/8",
    integrations=[DjangoIntegration()],
    environment="produccion",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    release=os.environ.get('GIT_COMMIT_SHA', 'release_desconocido')
)
