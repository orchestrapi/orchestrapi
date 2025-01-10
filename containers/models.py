import logging

from django.db.models import JSONField
from django.db import models
from django.db.models.signals import m2m_changed

from apps.models import App
from clients.docker import DockerClient
from core.behaviours import TimestampableBehaviour, UUIDIndexBehaviour
from core.mixins import SerializeMixin
from images.models import Image
from networks.models import NetworkBridge

logger = logging.getLogger("containers.models")


class ContainerBase(TimestampableBehaviour, UUIDIndexBehaviour, models.Model):

    container_id = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=30)
    params = JSONField(default=dict, blank=True)

    def __init__(self, *args, **kwargs):
        self.dclient = DockerClient()
        super(ContainerBase, self).__init__(*args, **kwargs)

    @property
    def inspect(self):
        if self.status:
            return self.dclient.inspect(self)

    @property
    def ip(self):
        if self.status and self.status not in ["stopped", "exited"]:
            return self.inspect["NetworkSettings"]["IPAddress"]

    def is_running(self):
        return self.status and self.status not in ["stopped", "exited"]

    class Meta:
        abstract = True


class Container(SerializeMixin, ContainerBase):

    instance_number = models.SmallIntegerField()
    app = models.ForeignKey(
        App, blank=True, null=True, related_name="containers", on_delete=models.CASCADE
    )
    image = models.ForeignKey(
        Image,
        blank=True,
        null=True,
        related_name="containers",
        on_delete=models.CASCADE,
    )
    networks = models.ManyToManyField(
        NetworkBridge, related_name="containers", blank=True
    )
    active = models.BooleanField(default=True)

    @property
    def status(self):
        if self.container_id and self.active:
            status = self.dclient.container_status(self.container_id)
            return status if status else "stopped"
        return None

    @property
    def port(self):
        return self.app.data.get("port", 8080)

    def start(self, instance_name=None):
        if not self.active:
            return
        self.dclient.docker_start(self, instance_name=instance_name)
        if not self.container_id:
            cont_id = self.dclient.container_id(self)
            if cont_id:
                self.container_id = cont_id
                self.save()

        if not self.networks.exists() and self.app.project.network:
            self.networks.add(self.app.project.network)

    def delete(self, **kwargs):
        self.dclient.remove(self)
        return super(Container, self).delete(**kwargs)

    def stop_all(self):
        instances = Container.objects.filter(image=self.image)
        for instance in instances:
            instance.stop()

    def stop(self):
        self.dclient._stop(self)


# SIGNALS


def connect_or_disconnect_container_to_network(
    sender, instance, action, model, pk_set, **kwargs
):
    if action in ["post_add", "post_remove"]:
        docker_container = instance.dclient.get_container_by_name(instance.container_id)
        networks_id = [str(pk) for pk in pk_set]
        networks_instances = model.objects.filter(id__in=networks_id)
        docker_networks = [
            instance.dclient.get_network_by_id(net.network_id)
            for net in networks_instances
        ]
        if action == "post_add":
            for network in docker_networks:
                logger.debug(
                    "Metiendo el contenedor %s en la red %s",
                    instance.name,
                    network.name,
                )
                instance.dclient.connect_container_to_network(network, docker_container)
                logger.debug(
                    "Contenedores presentes %s",
                    instance.dclient.get_containers_on_network(network),
                )
        elif action == "post_remove":
            for network in docker_networks:
                logger.debug(
                    "Sacando el contenedor %s de la red %s", instance.name, network.name
                )
                instance.dclient.disconnect_container_to_network(
                    network, docker_container
                )
                logger.debug(
                    "Contenedores presentes %s",
                    instance.dclient.get_containers_on_network(network),
                )


m2m_changed.connect(
    connect_or_disconnect_container_to_network, sender=Container.networks.through
)
