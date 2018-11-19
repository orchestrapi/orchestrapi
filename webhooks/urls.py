
from django.urls import path

from .views import manage_repository_webhook

urlpatterns = [
    path('<str:repository>/<str:app_id>', manage_repository_webhook),
]
