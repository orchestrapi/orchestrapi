from rest_framework import viewsets

from .models import Project
from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def __init__(self, *args, **kwargs):
        self.http_method_names = [
            m for m in super(*args, **kwargs).http_method_names
            if m not in ['delete', 'put', 'patch']
        ]
