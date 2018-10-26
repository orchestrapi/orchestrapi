
def start_containers(modeladmin, request, queryset):
    for container in queryset:
        if container.status == 'stopped':
            container.start(container.name)

def stop_containers(modeladmin, request, queryset):
    for container in queryset:
        if container.status != 'stopped':
            container.stop()

start_containers.short_description = "Arranca contenedores que estén parados."
stop_containers.short_description = "Detiene contenedores en ejecución."