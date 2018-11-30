import graphene

from apps.schema import AppQuery
from containers.schema import ContainerQuery
from images.schema import ImageQuery


class Query(
        AppQuery, ContainerQuery,
        ImageQuery,
        graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
