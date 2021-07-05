from rest_framework import viewsets
from .models import Container
from .serializers import ContainerSerializer


class ContainerViewSet(viewsets.ModelViewSet):
    serializer_class = ContainerSerializer
    queryset = Container.objects.all()
    
    def __init__(self, *args, **kwargs):
        self.http_method_names = [
            m for m in super(*args, **kwargs).http_method_names
            if m not in ['delete', 'put', 'patch']
        ]
