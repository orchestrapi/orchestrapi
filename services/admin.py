from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from django.utils.safestring import mark_safe
from prettyjson import PrettyJSONWidget
from .actions import start_service, stop_service

from .models import Service


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name','service_with_tag', 'status']
    actions = [start_service,stop_service]

    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget}
    }


admin.site.register(Service, ServiceAdmin)
