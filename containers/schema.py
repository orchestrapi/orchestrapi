import graphene
from graphene_django.types import DjangoObjectType

from apis.types import ContainerListType, DataType

from .models import Container


class ContainerType(DjangoObjectType):

    params = DataType()
    status = graphene.String()

    class Meta:
        model = Container

    def resolve_status(self, info):
        return self.status


class ContainerQuery:
    all_containers = graphene.List(ContainerType)
    container = graphene.Field(
        ContainerType,
        id=graphene.UUID())

    def resolve_all_containers(self, info, **kwargs):
        return Container.objects.all()

    def resolve_container(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Container.objects.get(id=id)
