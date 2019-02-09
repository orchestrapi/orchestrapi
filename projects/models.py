from django.db import models

from core.behaviours import (SlugableBehaviour, TimestampableBehaviour,
                             UUIDIndexBehaviour)
from core.mixins import SerializeMixin
from networks.models import NetworkBridge


class Project(UUIDIndexBehaviour, SlugableBehaviour, TimestampableBehaviour, SerializeMixin, models.Model):

    name = models.CharField(max_length=30)

    network = models.ForeignKey(NetworkBridge, related_name="projects",
                                on_delete=models.DO_NOTHING, blank=True, null=True)
