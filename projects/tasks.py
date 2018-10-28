
from clients.docker import DockerClient as dclient
from clients.git import GitClient as gclient
from core.celery import app

from .models import Project


@app.task()
def git_clone_task(project_id):
    project = Project.objects.get(id=project_id)
    if not project.cloned:
        gclient.clone(project)
        project.cloned = True
        project.save()

@app.task()
def git_update_task(project_id):
    project = Project.objects.get(id=project_id)
    gclient.update(project)

@app.task()
def docker_build_task(project_id):
    project = Project.objects.get(id=project_id)
    dclient.build(project)

@app.task()
def project_full_deploy_task(project_id):
    project = Project.objects.get(id=project_id)
    project.full_deploy()

@app.task()
def project_clone_build_update(project_id):
    project = Project.objects.get(id=project_id)
    if not project.cloned:
        print(f"Clonando proyecto {project.name}")
        gclient.clone(project)
        project.cloned = True
        project.save()
    print(f"Construyendo imagen del proyecto {project.name}")    
    dclient.build(project)
    print(f"Desplagando todas las instancias del proyecto {project.name}")    
    project.full_deploy()
    