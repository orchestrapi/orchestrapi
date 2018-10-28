from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    'orchestra.paquito.ninja'
]

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# FILE SYSTEM

NGINX_ROUTE = '/etc/nginx/'
GIT_PROJECTS_ROUTE = '/home/pi/docker_projects/'