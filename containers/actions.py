from .tasks import restart_containers_task


def start_containers(modeladmin, request, queryset):
    for container in queryset:
        if container.status in ['stopped', 'exited']:
            container.start(container.name)


def stop_containers(modeladmin, request, queryset):
    for container in queryset:
        if container.status not in ['stopped', 'exited']:
            container.stop()


def restart_containers(modeladmin, request, queryset):
    restart_containers_task.delay(
        [container.container_id for container in queryset])


start_containers.short_description = "Arranca contenedores que estén parados"
stop_containers.short_description = "Detiene contenedores en ejecución"
restart_containers.short_description = "Reiniciar los contenedores seleccionados"
