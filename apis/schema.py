import graphene

from apps.schema import AppQuery
from containers.schema import ContainerQuery


class Query(
        AppQuery, ContainerQuery,
        graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
