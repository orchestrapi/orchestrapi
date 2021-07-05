from django.db import models

from apps.models import App
from clients.docker import DockerClient
from core.behaviours import TimestampableBehaviour, UUIDIndexBehaviour
from core.mixins import SerializeMixin

dclient = DockerClient()


class Image(TimestampableBehaviour, UUIDIndexBehaviour, SerializeMixin, models.Model):

    name = models.CharField(max_length=30)
    tag = models.CharField(max_length=30, blank=True,
                           null=True, default='latest')
    image_id = models.CharField(max_length=30, blank=True, null=True)
    size = models.CharField(max_length=30, blank=True, null=True)
    local_build = models.BooleanField(default=True)
    built = models.BooleanField(default=False)
    last_version = models.BooleanField(default=True)

    app = models.ForeignKey(App, related_name='images',
                            null=True, blank=True, on_delete=models.CASCADE)

    @property
    def image_tag(self):
        return '{}:{}'.format(self.name, self.tag)

    def build(self, git_name):
        if not self.image_id:
            if self.local_build:
                dclient.build_from_image_model(self, git_name)
            else:
                dclient.pull_from_dockerhub(self.image_tag)

            docker_image_id, size = dclient.image_id_and_size(f'{self.name}:{self.tag}')
            if docker_image_id:
                self.image_id = docker_image_id
            self.size = size
            self.built = True
            self.save()

    def __str__(self):
        return self.image_tag
