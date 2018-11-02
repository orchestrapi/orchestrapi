import os

from django.conf import settings

from clients import ShellClient
from clients.docker import DockerClient as dclient
from clients.git import GitClient as gclient
from clients.tasks import send_slack_message
from core.celery import app
from images.models import Image

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
    gclient.update(project.git_name)


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
    image = project.get_or_create_last_image()
    if not image.built:
        image.build(project.git_name)
    print(f"Desplagando todas las instancias del proyecto {project.name}")
    project.full_deploy()
    project_update_nginx_conf(project.id)


def generate_conf_name(project_slug):
    # TODO: que el nombre de archivo que genere sea 001.basic en vez de basic
    return project_slug


@app.task()
def project_update_nginx_conf(project_id):
    project = Project.objects.get(id=project_id)
    rendered = project.render_nginx_conf()
    if not rendered:
        send_slack_message.delay('clients/slack/error_updating_nginx_conf.txt', {
            'project': {
                'name': project.name
            }
        })
        # TODO: Mandar un log
        return

    filename = generate_conf_name(project.slug)
    conf_file_name = f'{settings.NGINX_ROUTE}/sites-available/{filename}'
    with open(conf_file_name, 'w') as f:
        print(rendered, file=f)

    site_enabled_route = f'{settings.NGINX_ROUTE}/sites-enabled/{filename}'
    if not settings.DEBUG:
        if not os.path.exists(site_enabled_route):
            ShellClient.call(
                ['sudo', 'ln', '-s', conf_file_name, site_enabled_route])
        ShellClient.call(['sudo', 'service', 'nginx', 'restart'])
        send_slack_message.delay('clients/slack/successfull_nginx_restart.txt', {
            'project': {
                'name': project.name
            }
        })


@app.task()
def project_build_last_image(image_id, git_name):
    image = Image.objects.get(id=image_id)
    image.build(git_name)
    send_slack_message.delay('clients/slack/image_built.txt', {
        'image': {
            'name': image.name,
            'tag': image.tag,
            'size': image.size or "_/-\_",
            'local_build': image.local_build
        }
    })
