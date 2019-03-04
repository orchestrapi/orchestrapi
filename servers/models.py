from django.db import models
from core.behaviours import SlugableBehaviour, TimestampableBehaviour, UUIDIndexBehaviour
from core.mixins import SerializeMixin


class Server(SlugableBehaviour, TimestampableBehaviour, UUIDIndexBehaviour, SerializeMixin, models.Model):

    name = models.CharField(max_length=255, verbose_name="Name")
    location = models.GenericIPAddressField(verbose_name="Server IP Location")
    port = models.CharField(
        max_length=5, verbose_name="Daemon port", default="12001")

    @property
    def get_daemon_url(self):
        return f'http://{self.location}:{self.port}'

    def __str__(self):
        return f'{self.name} - {self.get_daemon_url}'
