import graphene
from graphene_django.types import DjangoObjectType

from apis.types import ContainerListType, DataType

from .models import App


class AppType(DjangoObjectType):

    data = DataType()
    params = DataType()
    domain = graphene.String()
    ready_to_publish = graphene.Boolean()
    last_version_registered = graphene.String()
    repository_type = graphene.String()
    cloned = graphene.Boolean()
    git = DataType()
    local_build = graphene.Boolean()
    stopped_containers = ContainerListType()
    running_containers = ContainerListType()

    def resolve_running_containers(self, *args):
        return self.running_containers

    def resolve_stopped_containers(self, *args):
        return self.stopped_containers

    def resolve_local_build(self, *args):
        return self.local_build

    def resolve_git(self, *args):
        return self.git

    def resolve_cloned(self, *args):
        return self.cloned

    def resolve_repository_type(self, *args):
        return self.repository_type

    def resolve_domain(self, *args):
        return self.domain

    def resolve_ready_to_publish(self, *args):
        return self.ready_to_publish

    def resolve_last_version_registered(self, *args):
        return self.last_version_registered

    class Meta:
        model = App


class AppQuery:
    all_apps = graphene.List(AppType)
    app = graphene.Field(
        AppType,
        id=graphene.UUID())

    def resolve_all_apps(self, *args, **kwargs):
        return App.objects.all()

    def resolve_app(self, *args, **kwargs):
        app_id = kwargs.get('id')

        if app_id is not None:
            return App.objects.get(id=app_id)
