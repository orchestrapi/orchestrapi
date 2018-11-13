from django.contrib import admin

from .models import Container

from .actions import start_containers, stop_containers


class ContainerAdmin(admin.ModelAdmin):
    list_display = ['container_id', 'name', '_image', 'ip', 'status', 'active']
    actions = [start_containers, stop_containers]
    list_filter = ['active', 'app']

    def _image(self, obj):
        if obj.image:
            return obj.image.image_tag
        return '-'


admin.site.register(Container, ContainerAdmin)
