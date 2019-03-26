from rest_framework.routers import DefaultRouter

from apps.viewsets import AppViewSet
from images.viewsets import ImageViewSet
from containers.viewsets import ContainerViewSet

router = DefaultRouter()
router.register(r'apps', AppViewSet, basename='apps')
router.register(r'images', ImageViewSet, basename='images')
router.register(r'containers', ContainerViewSet, base_name='containers')

urlpatterns = router.urls
