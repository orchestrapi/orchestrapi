from rest_framework import serializers

from .models import NetworkBridge


class NetworkBridgeSerializer(serializers.ModelSerializer):

    class Meta:
        model = NetworkBridge
        fields = ['id', 'name', 'network_id']
