from django.contrib.postgres.fields import JSONField
from django.db import models

from apps.models import App
from clients.docker import DockerClient
from core.behaviours import TimestampableBehaviour, UUIDIndexBehaviour
from images.models import Image

dclient = DockerClient()


class ContainerBase(TimestampableBehaviour, UUIDIndexBehaviour, models.Model):

    container_id = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=30)
    params = JSONField(default=dict, blank=True)

    @property
    def inspect(self):
        if self.status:
            return dclient.inspect(self)

    @property
    def ip(self):
        if self.status and self.status not in ['stopped', 'exited']:
            return self.inspect['NetworkSettings']['IPAddress']

    class Meta:
        abstract = True


class Container(ContainerBase):
    instance_number = models.SmallIntegerField()

    app = models.ForeignKey(
        App, blank=True, null=True,
        related_name='containers', on_delete=models.CASCADE)

    image = models.ForeignKey(
        Image, blank=True, null=True,
        related_name='containers', on_delete=models.CASCADE)

    active = models.BooleanField(default=True)

    @property
    def status(self):
        if self.container_id and self.active:
            status = dclient.container_status(self.container_id)
            return status if status else 'stopped'

    def start(self, instance_name=None):
        if not self.active:
            return
        result = dclient.docker_start(self, instance_name=instance_name)
        if not self.container_id:
            id = dclient.container_id(self)
            if id:
                self.container_id = id
                self.save()

    @property
    def port(self):
        return self.app.data.get('port', 8080)

    def delete(self, **kwargs):
        dclient.remove(self)
        return super(Container, self).delete(**kwargs)

    def stop_all(self):
        instances = Container.objects.filter(image=self.image)
        for instance in instances:
            instance.stop()

    def stop(self):
        dclient._stop(self)
