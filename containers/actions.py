from .tasks import restart_containers_task, stop_containers_task, start_containers_task


def start_containers(modeladmin, request, queryset):
    start_containers_task.delay(
        [container.pk for container in queryset if container.status in [
            'stopped', 'exited']]
    )


def stop_containers(modeladmin, request, queryset):
    stop_containers_task.delay(
        [container.pk for container in queryset if container.status not in [
            'stopped', 'exited']]
    )


def restart_containers(modeladmin, request, queryset):
    restart_containers_task.delay(
        [container.container_id for container in queryset])


start_containers.short_description = "Arranca contenedores que estén parados"
stop_containers.short_description = "Detiene contenedores en ejecución"
restart_containers.short_description = "Reiniciar los contenedores seleccionados"
