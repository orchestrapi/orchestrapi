from rest_framework import serializers

from .models import ConfigFile


class ConfigFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConfigFile
        fields = [
            'id', 'name', 'filename', 'content',
            'file', 'app', 'service'
        ]
