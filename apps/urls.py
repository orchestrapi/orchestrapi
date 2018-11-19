from .viewsets import AppViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'apps', AppViewSet, basename='apps')

urlpatterns = router.urls