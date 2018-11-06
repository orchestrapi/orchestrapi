import os

from django.conf import settings

from clients import ShellClient
from clients.docker import DockerClient as dclient
from clients.git import GitClient as gclient
from clients.tasks import send_slack_message
from core.celery import app
from images.models import Image

from .models import App

# TODO: Tarea para generar los certificados https
# sudo letsencrypt certonly --standalone -d loggerlady.paquito.ninja
# * Tarea para renover el certificado


@app.task()
def git_clone_task(app_id):
    app = App.objects.get(id=app_id)
    if not app.cloned:
        gclient.clone(app)
        app.cloned = True
        app.save()


@app.task()
def git_update_task(app_id):
    app = App.objects.get(id=app_id)
    gclient.update(app.git_name)


@app.task()
def docker_build_task(app_id):
    app = App.objects.get(id=app_id)
    dclient.build(app)


@app.task()
def app_full_deploy_task(app_id):
    app = App.objects.get(id=app_id)
    app.full_deploy()


@app.task()
def app_clone_build_update(app_id):
    app = App.objects.get(id=app_id)
    if not app.cloned:
        print(f"Clonando proyecto {app.name}")
        gclient.clone(app)
        app.cloned = True
        app.save()
    print(f"Construyendo imagen del proyecto {app.name}")
    image = app.get_or_create_last_image()
    if not image.built:
        image.build(app.git_name)
    print(f"Desplagando todas las instancias del proyecto {app.name}")
    app.full_deploy()
    app_update_nginx_conf(app.id)


def generate_conf_name(app_slug):
    # TODO: que el nombre de archivo que genere sea 001.basic en vez de basic
    return app_slug


@app.task()
def app_update_nginx_conf(app_id):
    app = App.objects.get(id=app_id)
    rendered = app.render_nginx_conf()
    if not rendered:
        send_slack_message.delay('clients/slack/error_updating_nginx_conf.txt', {
            'app': {
                'name': app.name
            }
        })
        # TODO: Mandar un log
        return

    filename = generate_conf_name(app.slug)
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
                'name': app.name
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
            'size': image.size or "_/-\_",
            'local_build': image.local_build
        }
    })
