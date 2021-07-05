import os
import logging

from django.conf import settings

from clients import ShellClient
from clients.docker import DockerClient
from clients.git import GitClient as gclient
from clients.tasks import send_slack_message
from core.celery import app
from images.models import Image

from .models import App

# TODO: Tarea para generar los certificados https
# sudo letsencrypt certonly --standalone -d loggerlady.paquito.ninja
# * Tarea para renover el certificado

DCLIENT = DockerClient()
logger = logging.getLogger('apps.tasks')

@app.task()
def git_clone_task(app_id):
    app_object = App.objects.get(id=app_id)
    if not app_object.cloned:
        gclient.clone(app_object)
        app_object.cloned = True
        app_object.save()


@app.task()
def git_update_task(app_id):
    app_object = App.objects.get(id=app_id)
    gclient.update(app_object.git.get("name"))


@app.task()
def docker_build_task(app_id):
    app_object = App.objects.get(id=app_id)
    DCLIENT.build(app_object)


@app.task()
def app_full_deploy_task(app_id):
    app_object = App.objects.get(id=app_id)
    app_object.full_deploy()


@app.task()
def app_clone_build_update(app_id):
    app_object = App.objects.get(id=app_id)
    if not app_object.cloned:
        gclient.clone(app)
        app_object.data['cloned'] = True
        app_object.save()
    image = app_object.get_or_create_last_image()
    if not image.built:
        image.build(app_object.git.get("name"))
    app_object.full_deploy()
    app_update_nginx_conf(app_object.id)


def generate_conf_name(app_slug):
    # TODO: que el nombre de archivo que genere sea 001.basic en vez de basic
    return app_slug


@app.task()
def app_update_nginx_conf(app_id):
    app_object = App.objects.get(id=app_id)
    rendered = app_object.render_nginx_conf()
    if not rendered:
        send_slack_message.delay('clients/slack/error_updating_nginx_conf.txt', {
            'app': {
                'name': app_object.name
            }
        })
        logger.error("Error updating nginx conf on app %s", app_object.slug)
        return
    filename = generate_conf_name(app_object.slug)
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
            'app': {
                'name': app_object.name
            }
        })


@app.task()
def app_build_last_image(image_id, git_name):
    image = Image.objects.get(id=image_id)
    image.build(git_name)
    send_slack_message.delay('clients/slack/image_built.txt', {
        'image': {
            'name': image.name,
            'tag': image.tag,
            'size': image.size or "?",
            'local_build': image.local_build
        }
    })
    app_update_instances_task(image.app.id)


@app.task()
def app_update_instances_task(app_id):
    app_object = App.objects.get(id=app_id)
    update_policy = app_object.data.get('update_policy', 'manual')

    if update_policy == 'manual':
        send_slack_message.delay('clients/slack/message.txt', {
            'message': f'Hay una nueva version que actualizar *manualmente* en el proyecto {app_object.name}.'
        })
        return

    send_slack_message.delay('clients/slack/message.txt', {
        'message': f'Comienza la actualización *automatica* de {app_object.name}.'
    })

    old_containers = app_object.containers.filter(active=True)
    if old_containers.exists():
        for old_cont in old_containers:
            old_cont.stop()
            old_cont.active = False
            if old_cont.networks.exists():
                for network in old_cont.networks.all():
                    old_cont.networks.remove(network)
            old_cont.save()
            DCLIENT.remove(old_cont)
            app_object.start_instance(old_cont.instance_number)
        if app_object.load_balancer:
            app_object.load_balancer.update_conf(app)
    else:
        app_object.full_deploy()

    send_slack_message.delay('clients/slack/message.txt', {
        'message': f'actualización *automatica* de {app_object.name} completada.'
    })
    app_update_nginx_conf(app_id)
