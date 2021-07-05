import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

sentry_sdk.init(
    dsn="https://dd867937f2e142fa9a39d1f0cedac357@sentry.io/1463061",
    integrations=[DjangoIntegration()]
)

DEBUG = False

ALLOWED_HOSTS = [
    os.environ.get('DOMAIN', 'example.com')
]

PROJECT_ROOT = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# FILE SYSTEM

NGINX_ROUTE = '/etc/nginx'
GIT_PROJECTS_ROUTE = os.environ.get('GIT_PROJECTS_ROUTE', '/path/to/git/apps')

# CORS

CORS_ORIGIN_WHITELIST = (
    os.environ.get('FRONT_APP_DOMAIN', 'example.com')
)

CSRF_TRUSTED_ORIGINS = (
    os.environ.get('FRONT_APP_DOMAIN', 'example.com')
)
