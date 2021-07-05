from rest_framework.routers import DefaultRouter

from apps.viewsets import AppViewSet
from containers.viewsets import ContainerViewSet
from files.viewsets import ConfigFileViewSet
from images.viewsets import ImageViewSet
from networks.viewsets import NetworkBridgeViewSet
from projects.viewsets import ProjectViewSet
from servers.viewsets import ServerViewSet

router = DefaultRouter()
router.register(r'apps', AppViewSet, base_name='apps')
router.register(r'images', ImageViewSet, base_name='images')
router.register(r'containers', ContainerViewSet, base_name='containers')
router.register(r'configfiles', ConfigFileViewSet, base_name='configfiles')
router.register(r'networks', NetworkBridgeViewSet, base_name='networks')
router.register(r'projects', ProjectViewSet, base_name='projects')
router.register(r'servers', ServerViewSet, base_name='servers')

urlpatterns = router.urls
