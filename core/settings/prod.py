from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    os.environ.get('DOMAIN', 'example.com')
]

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# FILE SYSTEM

NGINX_ROUTE = '/etc/nginx'
GIT_PROJECTS_ROUTE = os.environ.get('GIT_PROJECTS_ROUTE', '/path/to/git/projects')