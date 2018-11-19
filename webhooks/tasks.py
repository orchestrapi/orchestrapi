from core.celery import app

from apps.models import App
from images.models import Image
from clients.tasks import send_slack_message

from apps.tasks import app_build_last_image, app_update_instances_task


@app.task()
def process_github_webhook_task(message, app_id):
    import json
    send_slack_message.delay('clients/slack/message.txt', {
        'message': json.dums(message)})


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
            'domain': f'http://{app.domain}'
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
    app_update_instances_task(app_id)