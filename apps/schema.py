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

    def resolve_running_containers(self, info):
        return self.running_containers

    def resolve_stopped_containers(self, info):
        return self.stopped_containers

    def resolve_local_build(self, info):
        return self.local_build

    def resolve_git(self, info):
        return self.git

    def resolve_cloned(self, info):
        return self.cloned

    def resolve_repository_type(self, info):
        return self.repository_type

    def resolve_domain(self, info):
        return self.domain

    def resolve_ready_to_publish(self, info):
        return self.ready_to_publish

    def resolve_last_version_registered(self, info):
        return self.last_version_registered

    class Meta:
        model = App


class AppQuery:
    all_apps = graphene.List(AppType)
    app = graphene.Field(
        AppType,
        id=graphene.UUID())

    def resolve_all_apps(self, info, **kwargs):
        return App.objects.all()

    def resolve_app(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return App.objects.get(id=id)
