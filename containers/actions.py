
def start_containers(modeladmin, request, queryset):
    for container in queryset:
        if container.status in ['stopped', 'exited']:
            container.start(container.name)


def stop_containers(modeladmin, request, queryset):
    for container in queryset:
        if container.status not in ['stopped', 'exited']:
            container.stop()


start_containers.short_description = "Arranca contenedores que estén parados."
stop_containers.short_description = "Detiene contenedores en ejecución."
