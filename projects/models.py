from django.contrib.postgres.fields import JSONField
from django.db import models
from django.template import Context, loader

from core.behaviours import (SlugableBehaviour, TimestampableBehaviour,
                             UUIDIndexBehaviour)


class Project(SlugableBehaviour, TimestampableBehaviour, UUIDIndexBehaviour, models.Model):

    name = models.CharField(max_length=255, verbose_name="Name")
    git_url = models.URLField(blank=True, null=True)
    git_name = models.CharField(max_length=50, blank=True, null=True)
    domain = models.CharField(max_length=255, blank=True, null=True)
    data = JSONField(default=dict(), blank=True)
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

    def render_nginx_conf(self):
        if self.ready_to_publish:
            template = loader.get_template('projects/nginx/base.conf')
            ctx = {
                "containers": [cont for cont in self.containers.all() if cont.status != 'stopped'],
                "project_slug": self.slug,
                "domains": self.domain,
                "base_route": '/home/pi/webs'
            }
            return template.render(ctx)


    def raise_instance(self):
        from containers.models import Container
        num_cont_actives = self.containers.filter(active=True).count() + 1
        if self.containers.filter(active=True).exists():
            params = self.containers.filter(active=True).order_by('instance_number').last().params
            params['e']['INSTANCE'] = num_cont_actives
        else:
            params = {
                "e":{
                    "INSTANCE": num_cont_actives
                }
            }

        name = f'{self.slug}_{num_cont_actives}'
        version = self.data.get('version', 'latest')

        if self.data.get('local_build'):
            image = f'local/{self.slug}'
        else:
            image = f'{self.data.get("image", self.slug)}'
        try:
            instance = Container.objects.get(name=name)
        except Exception:
            instance = Container.objects.create(
                name=name, image=image, instance_number=num_cont_actives,
                version=version, params=params, project=self
            )

        instance.start()

    def scale(self, num_of_instances):
        if self.data.get('max_instances', 1) < num_of_instances or num_of_instances < 0:
            return
        instances = self.running_containers.order_by('-instance_number')
        if num_of_instances > instances.count():
            start_num_of_instances = instances.count() if instances.count() > 0 else 1
            for i in range(start_num_of_instances, num_of_instances + 1):
                print(f"Va a levantarse la instancia {i}")
                self.raise_instance()
        elif num_of_instances == instances.count():
            print(f"Ya estan levantadas las {num_of_instances} instancias!")
        else:
            to_stop_instances = instances.count() - num_of_instances
            instances_to_stop = instances[:to_stop_instances]
            for instance in instances_to_stop:
                print(f"Se va a parar {instance.name}")
                instance.stop()

    def full_deploy(self):
        return self.scale(self.data.get('max_instances', 1))

    def full_stop(self):
        instances = self.running_containers
        for instance in instances:
            instance.stop()
