from django.contrib import admin

from .models import Container

from .actions import start_containers, stop_containers

class ContainerAdmin(admin.ModelAdmin):
    list_display = ['container_id', 'name', 'image', 'version', 'ip','status']
    actions = [start_containers, stop_containers]

admin.site.register(Container, ContainerAdmin)