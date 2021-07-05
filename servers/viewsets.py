from rest_framework import viewsets

from .models import Server
from .serializers import ServerSerializer


class ServerViewSet(viewsets.ModelViewSet):

    queryset = Server.objects.all()
    serializer_class = ServerSerializer

    def __init__(self, *args, **kwargs):
        self.http_method_names = [
            m for m in super(*args, **kwargs).http_method_names
            if m not in ['delete', 'put', 'patch']
        ]
