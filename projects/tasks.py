
from core.celery import app
from clients.docker import DockerClient as dclient


@app.task()
def build_image_task(project_id):
    from .models import Project
    project = Project.objects.get(id=project_id)
    print(f"El proyecto {project.name} se esta contruyendo")
