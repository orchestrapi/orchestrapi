import os
import django
from django.core.handlers.wsgi import WSGIHandler


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.prod")
django.setup(set_prefix=False)

application = WSGIHandler()
