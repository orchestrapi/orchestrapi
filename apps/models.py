from django.contrib.postgres.fields import JSONField
from django.db import models
from django.template import loader
from django.conf import settings

from clients.tasks import send_slack_message
from core.behaviours import (SlugableBehaviour, TimestampableBehaviour,
                             UUIDIndexBehaviour)

from projects.models import Project
from core.mixins import SerializeMixin

def default_data():
    return {
        'cloned': False,
        'local_build': True,
        'max_instances': 1,
        'ssl': True,
        'domain': 'example.com',
        'git': {
            'name': '',
            'url': ''
        }
    }


class App(SlugableBehaviour, TimestampableBehaviour, UUIDIndexBehaviour, SerializeMixin, models.Model):

    name = models.CharField(max_length=255, verbose_name="Name")
    data = JSONField(default=default_data, blank=True)
    params = JSONField(default=dict, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='apps', blank=True, null=True)

    @property
    def ready_to_publish(self):
        return self.git.get("url") != None and self.domain != None and self.running_containers.count() > 0

    @property
    def last_version_registered(self):
        image = self.images.get(last_version=True)
        return image.tag if image else '-'

    @property
    def repository_type(self):
        if '@bitbucket.org' in self.git.get('url'):
            return 'bitbucket'
        elif 'https://github.com' in self.git.get('url'):
            return 'github'

    @property
    def webhook_url(self):
        return f'{settings.ORCHESTRAPI_HTTP_SCHEMA}://{settings.ORCHESTRAPI_DOMAIN_AND_PORT}/webhooks/{self.repository_type}/{self.id}'

    @property
    def domain(self):
        return self.data.get('domain', None)

    @property
    def running_containers(self):
        instances = self.containers.all()
        stopped = []
        for instance in instances:
            if not instance.status or instance.status in ['stopped', 'exited']:
                stopped.append(instance.id)
        return instances.exclude(id__in=stopped)

    @property
    def cloned(self):
        return self.data.get('cloned', False)

    @property
    def git(self):
        return self.data.get('git', {})

    @property
    def local_build(self):
        return self.data.get('local_build', False)

    @property
    def stopped_containers(self):
        instances = self.containers.all()
        running = []
        for instance in instances:
            if instance.status and instance.status not in ['stopped', 'exited']:
                running.append(instance.id)
        return instances.exclude(id__in=running)

    def render_nginx_conf(self):
        if self.ready_to_publish:
            if self.data.get('ssl', False):
                template = loader.get_template('apps/nginx/ssl.conf')
            else:
                template = loader.get_template('apps/nginx/base.conf')
            ctx = {
                "containers": [cont for cont in self.containers.filter(active=True) if cont.status not in ['stopped', 'exited']],
                "app_slug": self.slug,
                "domains": self.domain,
                "base_route": settings.BASE_APPS_DIR
            }
            return template.render(ctx)

    def get_or_create_last_image(self):
        name = f'local/{self.slug}' if self.local_build else self.data.get(
            'image', 'noimage')
        image, created = self.images.get_or_create(
            name=name,
            tag=self.data.get('version', 'latest'),
            last_version=True)
        if created:
            self.images.filter(
                last_version=True).exclude(
                    id=image.id).update(last_version=False)
            image.name = name
            image.local_build = self.local_build
            image.tag = self.data.get('version', 'latest')
        return image

    def _create_instance(self, version, instance_number):
        image = self.images.get(
            tag=version,
            local_build=self.local_build,
            last_version=True)

        if not image.built:
            image.build(self.git.get('name'))

        params = self.params
        if params.get('e'):
            params['e']['INSTANCE'] = instance_number
        else:
            params['e'] = {'INSTANCE': instance_number}

        params['e']['VERSION'] = image.tag

        name = f'{self.slug}_{instance_number}'

        send_slack_message.delay('clients/slack/message.txt', {
            'message': f'Creando el contenedor {name}.'
        })
        return self.containers.model.objects.create(
            name=name, image=image, instance_number=instance_number,
            params=params, app=self
        )

    def start_instance(self, instance_number):
        from images.models import Image
        if self.containers.filter(name=f"{self.slug}_{instance_number}", active=True).exists():
            container = self.containers.get(
                name=f"{self.slug}_{instance_number}", active=True)
            send_slack_message.delay('clients/slack/message.txt', {
                'message': f'Ya existe el contenedor {self.slug}_{instance_number}. Arrancando!'
            })
            return container.start()

        instance = self._create_instance(
            self.get_or_create_last_image().tag, instance_number)
        return instance.start()

    def scale(self, num_of_instances):
        if self.data.get('max_instances', 1) < num_of_instances or num_of_instances < 0:
            return
        instances = self.running_containers.order_by('-instance_number')
        if num_of_instances > instances.count():
            start_num_of_instances = instances.first().instance_number + \
                1 if instances.count() > 0 else 1
            for i in range(start_num_of_instances, num_of_instances + 1):
                send_slack_message.delay('clients/slack/message.txt', {
                    'message': f'Va a levantarse la instancia {i}'
                })
                self.start_instance(i)
        elif num_of_instances == instances.count():
            send_slack_message.delay('clients/slack/message.txt', {
                'message': f'Ya estan levantadas las {num_of_instances} instancias!'
            })
        else:
            to_stop_instances = instances.count() - num_of_instances
            instances_to_stop = instances[:to_stop_instances]
            for instance in instances_to_stop:
                send_slack_message.delay('clients/slack/message.txt', {
                    'message': f'Se va a parar {instance.name}'
                })
                instance.stop()

    def full_deploy(self):
        return self.scale(self.data.get('max_instances', 1))

    def full_stop(self):
        instances = self.running_containers
        for instance in instances:
            instance.stop()
