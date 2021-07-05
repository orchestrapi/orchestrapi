from rest_framework import viewsets

from .models import NetworkBridge
from .serializers import NetworkBridgeSerializer


class NetworkBridgeViewSet(viewsets.ModelViewSet):
    queryset = NetworkBridge.objects.all()
    serializer_class = NetworkBridgeSerializer

    def __init__(self, *args, **kwargs):
        self.http_method_names = [
            m for m in super(*args, **kwargs).http_method_names
            if m not in ['delete', 'put', 'patch']
        ]
