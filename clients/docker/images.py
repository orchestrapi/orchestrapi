from django.conf import settings

from ..git import GitClient as gclient
from ..tasks import send_slack_message


class DockerImagesMixin:
    def build_from_image_model(self, image, git_name):
        """Builds a container using an Image instance."""
        if not image.app.cloned:
            send_slack_message.delay('clients/slack/message.txt', {
                'message': f'Va clonarse la app *{image.name}:{image.tag}*'
            })
            gclient.clone(image.app)
            image.app.data['cloned'] = True
            image.app.save()

        gclient.checkout_tag(git_name, image.tag)
        send_slack_message.delay('clients/slack/message.txt', {
            'message': f'Va construirse la imagen *{image.name}:{image.tag}*'
        })
        template = [
            'docker', 'build', '-t',
            f'{image.image_tag}',
            f'{settings.GIT_PROJECTS_ROUTE}/{git_name}/.']
        return self.call(template)
