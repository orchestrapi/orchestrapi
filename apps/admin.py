from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from django.utils.safestring import mark_safe
from prettyjson import PrettyJSONWidget

from .actions import build_last_image, deploy, update_nginx_conf
from .models import App


class AppAdmin(admin.ModelAdmin):
    list_display = ['name', '_instance_number',
                    '_image', '_version', '_domain', '_webhook']
    actions = [deploy, build_last_image, update_nginx_conf]
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget}
    }

    def _instance_number(self, obj):
        text = f"{obj.running_containers.count()}/{obj.data.get('max_instances', 1)}"
        return text

    def _image(self, obj):
        return obj.last_version_registered

    def _version(self, obj):
        containers = obj.containers.filter(active=True)
        versions = ','.join(list(set([c.image.tag for c in containers])))
        return f'{versions or "-"}'

    def _webhook(self, obj):
        return mark_safe(f'<a href="{obj.webhook_url}" target="_blank">Webhook</a>')

    def _domain(self, obj):
        return mark_safe(f'<a href="http://{obj.data.get("domain")}" target="_blank">{obj.data.get("domain")}</a>')

    _instance_number.short_description = 'Running Instances / Max instances'
    _version.short_description = 'Running Version(s)'
    _image.short_description = 'Última versión construida'


admin.site.register(App, AppAdmin)
