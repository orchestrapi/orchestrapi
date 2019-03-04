from django.db import models
from core.behaviours import SlugableBehaviour, TimestampableBehaviour, UUIDIndexBehaviour
from core.mixins import SerializeMixin


class OwnerGroup(SlugableBehaviour, TimestampableBehaviour, UUIDIndexBehaviour, SerializeMixin, models.Model):

    name = models.CharField(max_length=255, verbose_name="Name")
