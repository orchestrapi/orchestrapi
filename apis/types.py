from graphene.types import Scalar


class DataType(Scalar):

    @staticmethod
    def serialize(dt):
        return dt


class ContainerListType(Scalar):

    @staticmethod
    def serialize(queryset):
        return [{
                "container_id": instance.container_id,
                "name": instance.name,
                "image": instance.image.image_tag,
                "status": instance.status,
                "active": instance.active
                } for instance in queryset]
