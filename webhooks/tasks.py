from core.celery import app

from apps.models import App
from images.models import Image
from clients.tasks import send_slack_message

from apps.tasks import app_build_last_image, app_update_instances_task


@app.task()
def process_github_webhook_task(message, app_id):
    if not 'refs/tags/' in message.get('ref'):
        return

    app = App.objects.get(id=app_id)

    new_version = {
        'tag': message['ref'].replace('refs/tags/', '').replace('v', ''),
        'message': message['head_commit']['message'],
        'date': message['head_commit']['timestamp'],
        'author': {
            'username': message['head_commit']['committer']['username'],
            'full_name': message['head_commit']['committer']['name']
        },
        'app': {
            'name': app.name,
            'domain': f'{"https" if app.data.get("ssl", False) else "http"}://{app.domain}'
        }
    }
    app.data['version'] = new_version['tag']
    app.save()
    send_slack_message.delay('clients/slack/new_tag_message.txt', new_version)

    # Create image object and build
    Image.objects.filter(name=app.data.get('image'),
                         last_version=True).update(last_version=False)
    image = app.get_or_create_last_image()
    app_build_last_image(image.id, app.git.get("name"))


@app.task()
def process_bitbucket_webhook_task(message, app_id):
    changes = message['push']['changes'][0]['new']

    if not changes['type'] == 'tag':
        return

    app = App.objects.get(id=app_id)

    new_version = {
        'tag': changes['name'].replace('v', ''),
        'message': changes['message'].replace('\n', ''),
        'date': changes['date'],
        'author': {
            'username': changes['target']['author']['user']['username'],
            'full_name': changes['target']['author']['user']['display_name']
        },
        'app': {
            'name': app.name,
            'domain': f'{"https" if app.data.get("ssl", False) else "http"}://{app.domain}'
        }
    }

    app.data['version'] = new_version['tag']
    app.save()
    send_slack_message.delay('clients/slack/new_tag_message.txt', new_version)

    # Create image object and build
    Image.objects.filter(name=app.data.get('image'),
                         last_version=True).update(last_version=False)
    image = app.get_or_create_last_image()
    app_build_last_image(image.id, app.git.get("name"))


@app.task()
def process_webhook_task(repository, message, app_id):
    if repository == 'github':
        process_github_webhook_task(message, app_id)
    elif repository == 'bitbucket':
        process_bitbucket_webhook_task(message, app_id)
