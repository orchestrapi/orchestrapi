import os

from django.conf import settings

from clients.docker import DockerClient as dclient
from clients.git import GitClient as gclient
from clients import ShellClient
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

def generate_conf_name(project_slug):
    return project_slug

@app.task()
def project_update_nginx_conf(project_id):
    project = Project.objects.get(id=project_id)
    rendered = project.render_nginx_conf()
    if not rendered:
        # TODO: Mandar mensaje de slack diciendo que no se puede generar la conf
        # y un log
        return

    filename = generate_conf_name(project.slug)
    conf_file_name = f'{settings.NGINX_ROUTE}/sites-available/{filename}'
    with open(conf_file_name, 'w') as f:
        print(rendered, file=f)

    site_enabled_route = f'{settings.NGINX_ROUTE}/sites-enabled/{filename}'
    if not os.path.exists(site_enabled_route):
        ShellClient.call(['sudo','ln', '-s', conf_file_name, site_enabled_route])
    ShellClient.call(['sudo', 'service', 'nginx', 'restart'])