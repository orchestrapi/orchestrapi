from django.contrib import admin

from .models import Container

from .actions import start_containers, stop_containers, restart_containers


class ContainerAdmin(admin.ModelAdmin):
    list_display = ['container_id', 'name', '_image','_networks', '_ip', 'status', 'active']
    actions = [start_containers, stop_containers, restart_containers]
    list_filter = ['active', 'app']

    def _image(self, obj):
        if obj.image:
            return obj.image.image_tag
        return '-'

    def _networks(self, obj):
        return ','.join([net.name for net in obj.networks.all()])

    def _ip(self, obj):
        if obj.ip:
            return f'{obj.ip}:{obj.port}'
        return ''

    _ip.short_description = "Container IP (Local)"

admin.site.register(Container, ContainerAdmin)
