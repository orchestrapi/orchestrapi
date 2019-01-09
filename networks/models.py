from django.db import models

from core.behaviours import SlugableBehaviour, TimestampableBehaviour, UUIDIndexBehaviour
from clients.docker import DockerClient


class NetworkBase(UUIDIndexBehaviour, SlugableBehaviour, TimestampableBehaviour, models.Model):

    name = models.CharField(max_length=30)

    def __init__(self, *args, **kwargs):
        self.dclient = DockerClient()
        super(NetworkBase, self).__init__(*args, *kwargs)

    class Meta:
        abstract = True


class NetworkBridge(NetworkBase):

    def create_network(self):
        pass
