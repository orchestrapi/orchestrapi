from django.contrib import admin
from django.forms import JSONField
from prettyjson import PrettyJSONWidget
from .actions import start_service, stop_service

from .models import Service


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_with_tag', 'ip', '_networks', 'status']
    actions = [start_service, stop_service]

    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget}
    }

    def _networks(self, obj):
        return ','.join([net.name for net in obj.networks.all()])


admin.site.register(Service, ServiceAdmin)
