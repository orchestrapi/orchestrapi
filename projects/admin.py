from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Project

from .tasks import project_clone_build_update, project_build_last_image, project_update_nginx_conf

def deploy(modeladmin, request, queryset):
    """Funcion temporal para deployar"""
    for project in queryset:
        project_clone_build_update.delay(project.id)        

deploy.short_description = "Desplejar (Temporal)"

def build_last_image(modeladmin, request, queryset):
    """Constuye o pullea la ultima imagen de docker"""
    for project in queryset:
        image = project.get_or_create_last_image()
        project_build_last_image.delay(image.id, project.git_name)

build_last_image.short_description = "Construir ultima imagen"

def update_nginx_conf(modeladmin, request, queryset):
    """Actualiza la configuracion de NGINX"""
    for project in queryset:
        project_update_nginx_conf.delay(project.id)

update_nginx_conf.short_description = "Actualiza la configuracion de NGINX"

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', '_instance_number','_image', '_version', '_domain']
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
