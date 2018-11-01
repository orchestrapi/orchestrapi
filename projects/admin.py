from django.contrib import admin
from django.utils.safestring import mark_safe

from .actions import build_last_image, deploy, update_nginx_conf
from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', '_instance_number',
                    '_image', '_version', '_domain']
    actions = [deploy, build_last_image, update_nginx_conf]

    def _instance_number(self, obj):
        text = f"{obj.running_containers.count()}/{obj.data.get('max_instances', 1)}"
        return text

    def _image(self, obj):
        return obj.data.get('image', '-')

    def _version(self, obj):
        containers = obj.containers.filter(active=True)
        versions = ','.join(list(set([c.image.tag for c in containers])))
        return f'{versions}/{obj.last_version}'

    def _domain(self, obj):
        return mark_safe(f'<a href="http://{obj.domain}" target="_blank">{obj.domain}</a>')

    _instance_number.short_description = 'Running Instances / Max instances'
    _version.short_description = 'Running Version(s) / Last version'


admin.site.register(Project, ProjectAdmin)
