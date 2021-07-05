from rest_framework import serializers

from .models import Server


class ServerSerializer(serializers.ModelSerializer):

    daemon_url = serializers.SerializerMethodField()

    def get_daemon_url(self, obj):
        return obj.get_daemon_url

    class Meta:
        model = Server
        fields = ['id', 'name', 'location', 'port', 'daemon_url']
