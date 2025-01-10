from rest_framework.routers import DefaultRouter

from apps.viewsets import AppViewSet
from containers.viewsets import ContainerViewSet
from files.viewsets import ConfigFileViewSet
from images.viewsets import ImageViewSet
from networks.viewsets import NetworkBridgeViewSet
from projects.viewsets import ProjectViewSet
from servers.viewsets import ServerViewSet

router = DefaultRouter()
router.register(r'apps', AppViewSet, basename='apps')
router.register(r'images', ImageViewSet, basename='images')
router.register(r'containers', ContainerViewSet, basename='containers')
router.register(r'configfiles', ConfigFileViewSet, basename='configfiles')
router.register(r'networks', NetworkBridgeViewSet, basename='networks')
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'servers', ServerViewSet, basename='servers')

urlpatterns = router.urls
