from .viewsets import AppViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'app', AppViewSet, basename='apps')

urlpatterns = router.urls