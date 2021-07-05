from rest_framework import serializers
from .models import App


class AppSerializer(serializers.ModelSerializer):
    repository_type = serializers.SerializerMethodField()

    class Meta:
        model = App
        fields = ['id', 'name', 'data', 'params',
                  'repository_type', 'create_date', 'slug']

    def get_repository_type(self, obj):
        try:
            return obj.repository_type
        except Exception:
            return ''
