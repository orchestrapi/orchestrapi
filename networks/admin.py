from django.contrib import admin

from .models import NetworkBridge


class NetworkBridgeAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name', 'network_id', '_num_of_containers']

    def _num_of_containers(self, obj):
        return len(obj.get_containers_list())


admin.site.register(NetworkBridge, NetworkBridgeAdmin)
