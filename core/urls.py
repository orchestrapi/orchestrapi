
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('webhooks/', include('webhooks.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include('apps.urls')),
    path('admin/', admin.site.urls),
]
