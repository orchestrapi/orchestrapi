from django.conf import settings

from clients.docker import DockerClient
from core.celery import app

dclient = DockerClient()

from .models import Service

@app.task()
def run_service_task(service_id):
    service = Service.objects.get(id=service_id)
    service.run()


@app.task()
def stop_service_task(service_id):
    service = Service.objects.get(id=service_id)
    service.stop()