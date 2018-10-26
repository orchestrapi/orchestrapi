from django.db import models

from django.contrib.postgres.fields import JSONField
from clients.docker import DockerClient as dclient

from core.behaviours import UUIDIndexBehaviour, TimestampableBehaviour

from projects.models import Project


class Container(TimestampableBehaviour,UUIDIndexBehaviour, models.Model):

    container_id = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=30)
    image = models.CharField(max_length=30)
    version = models.CharField(max_length=20, default="latest")
    params = JSONField(default=dict, blank=True)
    instance_number = models.SmallIntegerField()

    project = models.ForeignKey(
        Project, blank=True, null=True,
        related_name='containers', on_delete=models.CASCADE)

    active = models.BooleanField(default=True)

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


    @property
    def inspect(self):
        return dclient.inspect(self)

    @property
    def ip(self):
        if self.status and self.status != 'stopped':
            return self.inspect['NetworkSettings']['IPAddress']
        return None

    @property
    def port(self):
        return '8080'

    def remove(self):
        dclient.remove(self)

    def stop_all(self):
        instances = Container.objects.filter(image=self.image)
        for instance in instances:
            instance.stop()

    def stop(self):
        dclient._stop(self)
