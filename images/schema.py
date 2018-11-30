import graphene
from graphene_django.types import DjangoObjectType

from apis.types import ContainerListType, DataType

from .models import Image


class ImageType(DjangoObjectType):

    image_tag = graphene.String()

    def resolve_image_tag(self, info):
        return self.image_tag

    class Meta:
        model = Image


class ImageQuery:
    all_images = graphene.List(ImageType)
    image = graphene.Field(
        ImageType,
        id=graphene.UUID())

    def resolve_all_images(self, info, **kwargs):
        return Image.objects.all()

    def resolve_image(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Image.objects.get(id=id)
