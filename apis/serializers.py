"""Generic serializers module."""

from django.contrib.auth.models import Group, Permission, User
from rest_framework import serializers


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ['codename', 'name']

    def get_permissions_list(self, obj):
        return [perm.codename for perm in obj.permissions.all()]


class GroupSerializer(serializers.ModelSerializer):

    permissions = PermissionSerializer(many=True)
    permissions_list = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['name', 'permissions', 'permissions_list']

    def get_permissions_list(self, obj):
        return [perm.codename for perm in obj.permissions.all()]


class UserSerializer(serializers.ModelSerializer):

    groups = GroupSerializer(many=True)
    groups_list = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'groups', 'groups_list']

    def get_groups_list(self, obj):
        return [group.name for group in obj.groups.all()]

    def get_full_name(self, obj):
        return obj.get_full_name()
