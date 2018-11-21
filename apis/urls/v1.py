from django.urls import path, include


urlpatterns = [
    path('apps/', include('apps.urls'))
]
