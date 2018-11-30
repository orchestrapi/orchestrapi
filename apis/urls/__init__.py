from django.urls import path, include

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from graphene_django.views import GraphQLView
from django.conf import settings

from apis.schema import schema
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt

class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    pass


urlpatterns = [
    path('auth/token-auth/', obtain_jwt_token),
    path('auth/token-refresh/', refresh_jwt_token),
    path('auth/token-verify/', verify_jwt_token),
    path('auth/basic-auth/', include('rest_framework.urls')),

    path('graphql', csrf_exempt(PrivateGraphQLView.as_view(
        graphiql=settings.DEBUG
    ))),

    path('v1/', include('apis.urls.v1')),
]
