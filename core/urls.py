
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('webhooks/', include('webhooks.urls')),
    path('api/', include('apis.urls')),
    path('admin/', admin.site.urls),
]
