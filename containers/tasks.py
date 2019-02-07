from core.celery import app

from clients.docker import DockerClient

dclient = DockerClient()

@app.task()
def restart_containers_task(containers_ids):
    for container_id in containers_ids:
        docker_container = dclient.get_container_by_name(container_id)
        if docker_container and docker_container.status == 'running':
            print(f"Reiniciando contenedor: {container_id}")
            docker_container.restart()