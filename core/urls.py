
from django.contrib import admin
from django.urls import path, include

from .views import IndexView, DashboardView

urlpatterns = [
    path('', IndexView.as_view()),
    path('dashboard', DashboardView.as_view()),
    path('webhooks/', include('webhooks.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
