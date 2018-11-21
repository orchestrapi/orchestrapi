from rest_framework import viewsets
from .models import Container
from .serializers import ContainerSerializer


class ContainerViewSet(viewsets.ModelViewSet):
    serializer_class = ContainerSerializer
    queryset = Container.objects.all()
