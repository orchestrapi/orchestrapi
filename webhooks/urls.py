
from django.urls import path

from .views import manage_bitbucket_webhook, manage_github_webhook

urlpatterns = [
    path('bitbucket/<str:app_id>', manage_bitbucket_webhook),
    path('github/<str:app_id>', manage_github_webhook),
]
