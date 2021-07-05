from django.conf import settings
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from rest_framework_jwt.views import (obtain_jwt_token, refresh_jwt_token,
                                      verify_jwt_token)

urlpatterns = [
    path('auth/token-auth/', obtain_jwt_token),
    path('auth/token-refresh/', refresh_jwt_token),
    path('auth/token-verify/', verify_jwt_token),
    path('auth/basic-auth/', include('rest_framework.urls')),

    path('v1/', include('apis.urls.v1')),
]
