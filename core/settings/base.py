import os
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$-tk@aj!^k#l@*7k23an5x+26#@mq0pwv85o&-#)cau%=z8x9m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'prettyjson',
    'rest_framework',
    'corsheaders',
    'graphene_django',

    'clients',

    'apis.apps.ApisConfig',
    'apps.apps.AppsConfig',
    'containers.apps.ContainersConfig',
    'images.apps.ImagesConfig',
    'services.apps.ServicesConfig',
    'networks.apps.NetworksConfig',
    'projects.apps.ProjectsConfig',
    'servers.apps.ServersConfig',
    'owners.apps.OwnersConfig',
    'files.apps.FilesConfig',

    'webhooks.apps.WebhooksConfig'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'graphql_jwt.middleware.JSONWebTokenMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'database_name'),
        'USER': os.environ.get('DB_USER', 'database_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'database_password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

if 'TRAVIS' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql',
            'NAME':     'travisci',
            'USER':     'postgres',
            'PASSWORD': '',
            'HOST':     'localhost',
            'PORT':     '',
        }
    }

# Password validation

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

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media files
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CELERY

CELERY_BROKER_URL = os.environ.get(
    'RABBIT_URI', 'amqp://guest:guest@localhost:5672/')

# FILE SYSTEM

NGINX_ROUTE = os.path.join(BASE_DIR, '../conf-dev/nginx')
GIT_PROJECTS_ROUTE = os.path.join(BASE_DIR, '../conf-dev/git')
BASE_APPS_DIR = os.environ.get('BASE_APPS_DIR', '/home/pi/webs')

# SLACK

SLACK_BOT_ACTIVE = os.environ.get('SLACK_BOT_ACTIVE', 'False') == 'True'
SLACKBOT_KEY = os.environ.get('SLACKBOT_KEY', 'your-token')
SLACKBOT_SECRET = os.environ.get('SLACKBOT_SECRET', 'your-secret')

# Login / Logout settings

LOGOUT_REDIRECT_URL = '/'

# ORCHESTRA PI DOMAIN

ORCHESTRAPI_DOMAIN_AND_PORT = os.environ.get(
    'ORCHESTRAPI_DOMAIN_AND_PORT', 'localhost:8000')
ORCHESTRAPI_HTTP_SCHEMA = os.environ.get('ORCHESTRAPI_HTTP_SCHEMA', 'http')

# CORS

CORS_ORIGIN_WHITELIST = (
    'localhost:4200',
)

CSRF_TRUSTED_ORIGINS = (
    'localhost:4200',
)

# REST FRAMEWORK

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}

# REST FRAMEWORK JWT

JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'apis.handlers.jwt_response_payload_handler',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=1),
    'JWT_ALLOW_REFRESH': True,
}

# GRAPHENE

GRAPHENE = {
    'SCHEMA': 'apis.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware'
    ]
}

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]