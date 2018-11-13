from core.celery import app

from apps.models import App
from images.models import Image
from clients.tasks import send_slack_message

from apps.tasks import app_build_last_image


@app.task()
def process_github_webhook_task(message, app_id):
    pass


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
    image, created = Image.objects.get_or_create(
        name=app.data.get('image'), tag=new_version['tag'],
        local_build=app.data.get('local_build', True)
    )
    image.last_version = True
    image.save()
    app_build_last_image.delay(image.id, app.git.get("name"))


@app.task()
def process_webhook_task(repository, message, app_id):
    if repository == 'github':
        process_github_webhook_task.delay(message, app_id)
    elif repository == 'bitbucket':
        process_bitbucket_webhook_task.delay(message, app_id)
