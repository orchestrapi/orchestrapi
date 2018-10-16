from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    'orchestra.paquito.ninja'
]

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

print(STATIC_ROOT)