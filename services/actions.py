from .tasks import run_service_task, stop_service_task

def start_service(modeladmin, request, queryset):
    for service in queryset:
        if service.status not in ['running']:
            run_service_task(service.id)

def stop_service(modeladmin, request, queryset):
    for service in queryset:
        if service.status not in ['stopped', 'exited']:
            stop_service_task.delay(service.id)


start_service.short_description = "Arranca el servicio seleccionado."
stop_service.short_description = "Detiene el servicio seleccionado."