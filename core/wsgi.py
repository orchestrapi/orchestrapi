import os
import django
from django.core.handlers.wsgi import WSGIHandler


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.production")
django.setup(set_prefix=False)

application = WSGIHandler()
