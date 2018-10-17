from django.db import models

from django.contrib.postgres.fields import JSONField
from dockerclient import DockerClient as dclient


class Container(models.Model):
    
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

    def start(self):
        dclient.docker_start(self)
        if not self.container_id:
            id = dclient.container_id(self)
            if id:
                self.container_id = id
                self.save()

    def stop(self):
        dclient._stop(self)