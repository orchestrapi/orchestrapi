from rest_framework import serializers

from .models import Image


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['id', 'name', 'tag', 'image_id', 'size',
                  'local_build', 'built', 'last_version', 'app']
