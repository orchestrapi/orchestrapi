from django.db import models

from django.contrib.postgres.fields import JSONField
from clients.docker import DockerClient

from core.behaviours import UUIDIndexBehaviour, TimestampableBehaviour


class Container(TimestampableBehaviour,UUIDIndexBehaviour, models.Model):

    container_id = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=30)
    image = models.CharField(max_length=30)
    version = models.CharField(max_length=20, default="latest")
    params = JSONField(default=dict, blank=True)

    @property
    def status(self):
        if self.container_id:
            status = dclient.container_status(self.container_id)
            return status if status else 'stopped'
        return None

    def start(self, instance_name=None):
        result = dclient.docker_start(self, instance_name=instance_name)
        if not self.container_id:
            id = dclient.container_id(self.name)
            if id:
                self.container_id = id
                self.save()

    def raise_instance(self, instance_number):
        params =self.params
        params['e'] = f'INSTANCE={instance_number}'
        name = self.name.split("_")[0] + f"_{instance_number}"
        try:
            instance = Container.objects.get(name=name)
        except Exception:
            instance = Container.objects.create(
                name = name, image = self.image,
                version = self.version, params=params
            )
        instance.start()

    def running_instances(self):
        """Esto deberia ir a un manager"""
        instances = Container.objects.filter(image=self.image).order_by('name')
        stopped = []
        for instance in instances:
            if not instance.status or instance.status == 'stopped':
                stopped.append(instance.id)
        return instances.exclude(id__in=stopped)

    def scale(self, instance_number):
        instances = self.running_instances().order_by('-name')
        if instance_number > instances.count():
            start_instance_number = instances.count() if instances.count() > 0 else 1
            for i in range(start_instance_number, instance_number + 1):
                print(f"Va a levantarse la instancia {i}")
                self.raise_instance(i)
        elif instance_number == instances.count():
            print(f"Ya estan levantadas las {instance_number} instancias!")
        else:
            to_stop_instances = instances.count() - instance_number
            instances_to_stop = instances[:to_stop_instances]
            for instance in instances_to_stop:
                print(f"Se va a parar {instance.name}")
                instance.stop()

    @property
    def inspect(self):
        return dclient.inspect(self)

    @property
    def ip(self):
        if self.status and self.status != 'stopped':
            return self.inspect['NetworkSettings']['IPAddress']
        return None

    def remove(self):
        dclient.remove(self)

    def stop_all(self):
        instances = Container.objects.filter(image=self.image)
        for instance in instances:
            instance.stop()

    def stop(self):
        dclient._stop(self)
