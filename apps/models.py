from django.contrib.postgres.fields import JSONField
from django.db import models
from django.template import loader

from clients.tasks import send_slack_message
from core.behaviours import (SlugableBehaviour, TimestampableBehaviour,
                             UUIDIndexBehaviour)


class App(SlugableBehaviour, TimestampableBehaviour, UUIDIndexBehaviour, models.Model):

    name = models.CharField(max_length=255, verbose_name="Name")
    git_url = models.URLField(blank=True, null=True)
    git_name = models.CharField(max_length=50, blank=True, null=True)
    domain = models.CharField(max_length=255, blank=True, null=True)
    data = JSONField(default=dict, blank=True)
    last_version = models.CharField(max_length=30, default="latest")
    params = JSONField(default=dict, blank=True)
    cloned = models.BooleanField(default=False)

    @property
    def ready_to_publish(self):
        return self.git_url != None and self.domain != None and self.running_containers.count() > 0

    @property
    def running_containers(self):
        instances = self.containers.all()
        stopped = []
        for instance in instances:
            if not instance.status or instance.status == 'stopped':
                stopped.append(instance.id)
        return instances.exclude(id__in=stopped)

    @property
    def stopped_containers(self):
        instances = self.containers.all()
        running = []
        for instance in instances:
            if instance.status and instance.status != 'stopped':
                running.append(instance.id)
        return instances.exclude(id__in=running)

    def render_nginx_conf(self):
        if self.ready_to_publish:
            if self.data.get('ssl', False):
                template = loader.get_template('apps/nginx/ssl.conf')
            else:
                template = loader.get_template('apps/nginx/base.conf')
            ctx = {
                "containers": [cont for cont in self.containers.all() if cont.status != 'stopped'],
                "app_slug": self.slug,
                "domains": self.domain,
                "base_route": '/home/pi/webs'
            }
            return template.render(ctx)

    def get_or_create_last_image(self):
        image, created = self.images.get_or_create(
            name=self.data['image'], tag=self.last_version,
            local_build=self.data.get('local_build', False),
            last_version=True
        )
        if created:
            self.images.objects.filter(
                name=self.data['image'], last_version=True).exclude(
                    id=image.id).update(last_version=False)
        return image

    def _create_instance(self, version, instance_number):
        image = self.images.get(
            name=self.data['image'], tag=version,
            local_build=self.data.get('local_build', False),
            last_version=True)

        if not image.built:
            image.build(self.git_name)

        params = self.params
        if params.get('e'):
            params['e']['INSTANCE'] = instance_number
        else:
            params['e'] = {'INSTANCE': instance_number}

        params['e']['VERSION'] = image.tag

        name = f'{self.slug}_{instance_number}'

        print(f"Creando el contenedor {name}. Guardando!")
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
            # ya existe el contenedor
            container = self.containers.get(
                name=f"{self.slug}_{instance_number}", active=True)
            print(
                f"Ya existe el contenedor {self.slug}_{instance_number}. Arrancando!")
            send_slack_message.delay('clients/slack/message.txt', {
                'message': f'Ya existe el contenedor {self.slug}_{instance_number}. Arrancando!'
            })
            return container.start()

        # hay q crearlo
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
                print(f"Va a levantarse la instancia {i}")
                send_slack_message.delay('clients/slack/message.txt', {
                    'message': f'Va a levantarse la instancia {i}'
                })
                self.start_instance(i)
        elif num_of_instances == instances.count():
            print(f"Ya estan levantadas las {num_of_instances} instancias!")
            send_slack_message.delay('clients/slack/message.txt', {
                'message': f'Ya estan levantadas las {num_of_instances} instancias!'
            })
        else:
            to_stop_instances = instances.count() - num_of_instances
            instances_to_stop = instances[:to_stop_instances]
            for instance in instances_to_stop:
                print(f"Se va a parar {instance.name}")
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
