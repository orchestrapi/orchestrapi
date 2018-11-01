from core.celery import app

from projects.models import Project
from clients.tasks import send_slack_message

def is_new_version_webhook(changes):
    return changes['type'] == 'tag'


@app.task()
def process_webhook(message, project_id):
    changes = message['push']['changes'][0]['new']

    if not is_new_version_webhook(changes):
        return

    project = Project.objects.get(id=project_id)

    new_version = {
        'tag': changes['name'].replace('v', ''),
        'message': changes['message'].replace('\n', ''),
        'date': changes['date'],
        'author': {
            'username': changes['target']['author']['user']['username'],
            'full_name': changes['target']['author']['user']['display_name']
        },
        'project': {
            'name': project.name,
            'domain': f'http://{project.domain}'
        }
    }

    project.last_version = new_version['tag']
    project.save()
    send_slack_message.delay('clients/slack/new_tag_message.txt', new_version)
