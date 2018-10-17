from django.contrib import admin

from .models import Container

class ContainerAdmin(admin.ModelAdmin):
    list_display = ['container_id', 'name', 'image', 'version', 'status']


admin.site.register(Container, ContainerAdmin)