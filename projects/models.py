from django.db import models

from django.contrib.postgres.fields import JSONField

from core.behaviours import UUIDIndexBehaviour, TimestampableBehaviour, SlugableBehaviour


class Project(SlugableBehaviour, TimestampableBehaviour,UUIDIndexBehaviour, models.Model):

    name = models.CharField(max_length=255, verbose_name="Name")
