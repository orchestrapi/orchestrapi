from django.db import models

from core.behaviours import UUIDIndexBehaviour, TimestampableBehaviour
from clients.docker import DockerClient as dclient

class Image(TimestampableBehaviour, UUIDIndexBehaviour, models.Model):

    name = models.CharField(max_length=30)
    tag = models.CharField(max_length=30, blank=True, null=True, default='latest')
    image_id = models.CharField(max_length=30, blank=True, null=True)
    size = models.CharField(max_length=30, blank=True, null=True)
    local_build = models.BooleanField(default=True)
    built = models.BooleanField(default=False)
    last_version = models.BooleanField(default=True)

    @property
    def image_tag(self):
        return '{}:{}'.format(self.name, self.tag)

    def build(self, git_name):
        if not self.image_id:
            if self.local_build:
                dclient.build_from_image_model(self, git_name)
            else:
                dclient.pull_from_dockerhub(self.image_tag)

            id, size = dclient.image_id_and_size(f'{self.name}:{self.tag}')
            if id:
                self.image_id = id
            self.size = size
            self.built = True
            self.save()

    def __str__(self):
        return self.image_tag