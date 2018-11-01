from .tasks import project_clone_build_update, project_build_last_image, project_update_nginx_conf


def deploy(modeladmin, request, queryset):
    """Funcion temporal para deployar"""
    for project in queryset:
        project_clone_build_update.delay(project.id)


def build_last_image(modeladmin, request, queryset):
    """Constuye o pullea la ultima imagen de docker"""
    for project in queryset:
        image = project.get_or_create_last_image()
        project_build_last_image.delay(image.id, project.git_name)


def update_nginx_conf(modeladmin, request, queryset):
    """Actualiza la configuracion de NGINX"""
    for project in queryset:
        project_update_nginx_conf.delay(project.id)


deploy.short_description = "Desplejar (Temporal)"
update_nginx_conf.short_description = "Actualiza la configuracion de NGINX"
build_last_image.short_description = "Construir ultima imagen"
