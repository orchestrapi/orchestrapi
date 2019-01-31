from django.db import models

from core.behaviours import SlugableBehaviour, TimestampableBehaviour, UUIDIndexBehaviour
from clients.docker import DockerClient

from django.db.models.signals import post_delete

class NetworkBase(UUIDIndexBehaviour, SlugableBehaviour, TimestampableBehaviour, models.Model):

    name = models.CharField(max_length=30)
    network_id = models.CharField(max_length=100, blank=True, null=True)

    def __init__(self, *args, **kwargs):
        self.dclient = DockerClient()
        super(NetworkBase, self).__init__(*args, *kwargs)

    def get_docker_network(self):
        if self.network_id:
            return self.dclient.get_network_by_id(self.network_id)

    def remove_docker_network(self):
        if self.network_id:
            network = self.get_docker_network()
            if network:
                self.dclient.remove_network(self.get_docker_network())

    class Meta:
        abstract = True


class NetworkBridge(NetworkBase):

    def save(self, *args, **kwargs):
        super(NetworkBridge, self).save(*args, **kwargs)
        if not self.network_id:
            self.create_network()

    def create_network(self):
        network = self.dclient.create_network(self.slug)
        self.network_id = network.id
        self.save()


# SIGNALS

def delete_docker_network(sender, **kwargs):
    instance = kwargs.get('instance')
    instance.remove_docker_network()

post_delete.connect(delete_docker_network, sender=NetworkBridge)