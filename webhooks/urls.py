
from django.urls import path

from .views import manage_webhook

urlpatterns = [
    path('<str:app_id>', manage_webhook),

]
