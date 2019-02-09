from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.signals import m2m_changed

from clients.docker import DockerClient
from containers.models import (ContainerBase,
                               connect_or_disconnect_container_to_network)
from core.behaviours import (SlugableBehaviour, TimestampableBehaviour,
                             UUIDIndexBehaviour)
from core.mixins import SerializeMixin
from networks.models import NetworkBridge

dclient = DockerClient()


def default_data():
    return {
        'max_instances': 1,
        'docker': {
            'name': '',
            'tag': ''
        }
    }


class Service(SlugableBehaviour, SerializeMixin, ContainerBase):

    data = JSONField(default=default_data, blank=True)
    networks = models.ManyToManyField(
        NetworkBridge, related_name="services", blank=True)

    @property
    def docker(self):
        return self.data.get('docker', {})

    @property
    def status(self):
        if self.container_id:
            status = dclient.container_status(self.container_id)
            return status if status else 'stopped'
        return None

    @property
    def service_with_tag(self):
        return f"{self.docker.get('name')}:{self.docker.get('tag')}"

    def run(self):
        dclient.docker_start(self)
        if not self.container_id:
            id = dclient.container_id(self)
            if id:
                self.container_id = id
                self.save()

    def stop(self):
        dclient._stop(self)

# SIGNALS


m2m_changed.connect(connect_or_disconnect_container_to_network,
                    sender=Service.networks.through)
