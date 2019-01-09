from django.db import models
from core.behaviours import SlugableBehaviour, TimestampableBehaviour, UUIDIndexBehaviour


class Project(UUIDIndexBehaviour, SlugableBehaviour, TimestampableBehaviour, models.Model):

    name = models.CharField(max_length=30)
