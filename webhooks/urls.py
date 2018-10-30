
from django.urls import path

from .views import manage_webhook

urlpatterns = [
    path('<str:project_id>', manage_webhook),

]
