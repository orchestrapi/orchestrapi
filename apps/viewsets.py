
from rest_framework import viewsets

from .models import App
from .serializers import AppSerializer


class AppViewSet(viewsets.ModelViewSet):
    serializer_class = AppSerializer
    queryset = App.objects.all()

    def __init__(self, *args, **kwargs):
        self.http_method_names = [
            m for m in super(*args, **kwargs).http_method_names
            if m not in ['delete', 'put', 'patch']
        ]
