import logging

from clients.docker import DockerClient
from core.celery import app

from .models import Container

logger = logging.getLogger('containers.tasks')

dclient = DockerClient()


@app.task()
def restart_containers_task(containers_ids):
    for container_id in containers_ids:
        docker_container = dclient.get_container_by_name(container_id)
        if docker_container and docker_container.status == 'running':
            logger.info("Reiniciando contenedor: %s", container_id)
            docker_container.restart()


@app.task()
def stop_containers_task(containers_ids):
    containers = Container.objects.filter(id__in=containers_ids)
    for container in containers:
        container.stop()


@app.task()
def start_containers_task(containers_ids):
    containers = Container.objects.filter(id__in=containers_ids)
    for container in containers:
        container.start(container.name)
