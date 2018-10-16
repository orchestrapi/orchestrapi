from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    'orchestra.paquito.ninja'
]

MEDIA_ROOT = os.path.join(PROJECT_ROOT, '../media')
STATIC_ROOT = os.path.join(PROJECT_ROOT, '../static')
