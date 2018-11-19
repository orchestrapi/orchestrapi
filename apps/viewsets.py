
from .models import App
from .serializers import AppSerializer
from rest_framework import viewsets


class AppViewSet(viewsets.ModelViewSet):
    serializer_class = AppSerializer
    queryset = App.objects.all()