import logging
from datetime import datetime

from apps.models import App
from apps.tasks import app_build_last_image
from clients.tasks import send_slack_message
from core.celery import app
from images.models import Image


logger = logging.getLogger('webhooks.tasks')


@app.task()
def process_github_webhook_task(message, app_id):
    if not 'refs/tags/' in message.get('ref'):
        return

    app_instance = App.objects.get(id=app_id)

    new_version = {
        'tag': message['ref'].replace('refs/tags/', '').replace('v', ''),
        'message': message['head_commit']['message'],
        'date': message['head_commit']['timestamp'],
        'author': {
            'username': message['head_commit']['committer']['username'],
            'full_name': message['head_commit']['committer']['name']
        },
        'app': {
            'name': app_instance.name,
            'domain': f'{"https" if app_instance.data.get("ssl", False) else "http"}://{app_instance.domain}'
        }
    }
    app_instance.data['version'] = new_version['tag']
    app_instance.save()
    send_slack_message.delay('clients/slack/new_tag_message.txt', new_version)

    # Create image object and build
    Image.objects.filter(name=app_instance.data.get('image'),
                         last_version=True).update(last_version=False)
    image = app_instance.get_or_create_last_image()
    app_build_last_image(image.id, app.git.get("name"))


@app.task()
def process_bitbucket_webhook_task(message, app_id):
    changes = message['push']['changes'][0]['new']

    if not changes['type'] == 'tag':
        return

    app_instance = App.objects.get(id=app_id)

    new_version = {
        'tag': changes['name'].replace('v', ''),
        'message': changes['message'].replace('\n', ''),
        'date': changes['date'],
        'author': {
            'username': changes['target']['author']['user']['username'],
            'full_name': changes['target']['author']['user']['display_name']
        },
        'app': {
            'name': app_instance.name,
            'domain': f'{"https" if app_instance.data.get("ssl", False) else "http"}://{app_instance.domain}'
        }
    }

    app_instance.data['version'] = new_version['tag']
    app_instance.save()
    send_slack_message.delay('clients/slack/new_tag_message.txt', new_version)

    # Create image object and build
    Image.objects.filter(name=app_instance.data.get('image'),
                         last_version=True).update(last_version=False)
    image = app_instance.get_or_create_last_image()
    app_build_last_image(image.id, app_instance.git.get("name"))


@app.task()
def process_gitlab_webhook_task(message, app_id, headers):
    push_type_event = headers['HTTP_X_GITLAB_EVENT']
    app_instance = App.objects.get(id=app_id)
    if push_type_event == 'Tag Push Hook':
        # It is a new release     "ref": "refs/tags/v0.1",
        version = message['ref'].split('/')[2]
        new_version = {
            'tag': version.replace('v', ''),
            'message': message['message'].replace('\n', ''),
            'date': str(datetime.now()),
            'author': {
                'username': message['user_username'],
                'full_name': message['user_name']
            },
            'app': {
                'name': app_instance.name,
                'domain': f'{"https" if app_instance.data.get("ssl", False) else "http"}://{app_instance.domain}'
            }
        }
        app_instance.data['version'] = new_version['tag']
        app_instance.save()
        send_slack_message.delay('clients/slack/new_tag_message.txt', new_version)
        # Create image object and build
        Image.objects.filter(name=app_instance.data.get('image'),
                             last_version=True).update(last_version=False)
        image = app_instance.get_or_create_last_image()
        app_build_last_image(image.id, app_instance.git.get("name"))

    elif push_type_event == 'Push Hook':
        # a normal push to a branch
        logger.info("NORMAL PUSH")


@app.task()
def process_webhook_task(repository, message, app_id, headers=None):
    if repository == 'github':
        process_github_webhook_task.delay(message, app_id)
    elif repository == 'bitbucket':
        process_bitbucket_webhook_task.delay(message, app_id)
    elif repository == 'gitlab':
        process_gitlab_webhook_task.delay(message, app_id, headers)
