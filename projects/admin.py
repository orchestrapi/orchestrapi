from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Project

from .tasks import project_clone_build_update

def deploy(modeladmin, request, queryset):
    """Funcion temporal para deployar"""
    for project in queryset:
        project_clone_build_update.delay(project.id)        

deploy.short_description = "Desplejar (Temporal)"

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', '_instance_number','_image', '_version', '_domain']
    actions = [deploy]

    def _instance_number(self, obj):
        text = f"{obj.running_containers.count()}/{obj.data.get('max_instances', 1)}"
        return text

    def _image(self, obj):
        return obj.data.get('image', '-')

    def _version(self, obj):
        return obj.data.get('version', 'latest')

    def _domain(self, obj):
        return mark_safe(f'<a href="http://{obj.domain}" target="_blank">{obj.domain}</a>')

    _instance_number.short_description = 'Running Instances / Max instances'


admin.site.register(Project, ProjectAdmin)
