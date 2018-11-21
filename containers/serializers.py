from rest_framework import serializers

from .models import Container


class ContainerSerializer(serializers.ModelSerializer):

    ip = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_ip(self, obj):
        return obj.ip

    def get_status(self, obj):
        return obj.status

    class Meta:
        model = Container
        fields = ['id', 'container_id', 'ip', 'status',
                  'instance_number', 'app', 'image', 'active', 'params']
