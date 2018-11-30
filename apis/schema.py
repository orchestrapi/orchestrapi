import graphene
import graphql_jwt

from apps.schema import AppQuery
from containers.schema import ContainerQuery
from images.schema import ImageQuery


class Query(
        AppQuery, ContainerQuery,
        ImageQuery,
        graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
