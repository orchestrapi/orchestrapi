from .tasks import app_clone_build_update, app_build_last_image, app_update_nginx_conf


def deploy(modeladmin, request, queryset):  # noqa
    """Funcion temporal para deployar"""
    for app in queryset:
        app_clone_build_update.delay(app.id)


def build_last_image(modeladmin, request, queryset):  # noqa
    """Constuye o pullea la ultima imagen de docker"""
    for app in queryset:
        image = app.get_or_create_last_image()
        app_build_last_image.delay(image.id, app.git.get("name"))


def update_nginx_conf(modeladmin, request, queryset):  # noqa
    """Actualiza la configuracion de NGINX"""
    for app in queryset:
        app_update_nginx_conf.delay(app.id)


deploy.short_description = "Desplegar (Temporal)"
update_nginx_conf.short_description = "Actualiza la configuracion de NGINX"
build_last_image.short_description = "Construir ultima imagen"
