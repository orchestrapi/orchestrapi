from core.celery import app

from projects.models import Project
from images.models import Image
from clients.tasks import send_slack_message

from projects.tasks import project_build_last_image

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
    
    # Create image object and build
    Image.objects.filter(name=project.data.get('image'), last_version=True).update(last_version=False)
    image, created = Image.objects.get_or_create(
        name=project.data.get('image'), tag=new_version['tag'],
        local_build=project.data.get('local_build', True)
    )
    image.last_version = True
    image.save()
    project_build_last_image.delay(image.id, project.git_name)
