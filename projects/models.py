from django.db import models
from core.behaviours import SlugableBehaviour, TimestampableBehaviour, UUIDIndexBehaviour

from networks.models import NetworkBridge

class Project(UUIDIndexBehaviour, SlugableBehaviour, TimestampableBehaviour, models.Model):

    name = models.CharField(max_length=30)

    network = models.ForeignKey(NetworkBridge, related_name="projects", on_delete=models.DO_NOTHING, blank=True, null=True)
