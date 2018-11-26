"""Behaviours module."""
import uuid

from django.db import models
from django.utils.text import slugify


class TimestampableBehaviour(models.Model):
    """Defines fields for dates creation and update."""

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDIndexBehaviour(models.Model):
    """Uuid primary key for models."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class SlugableBehaviour(models.Model):
    """Adds a slug fields to models."""

    slugable_field = 'name'
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.slug

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(getattr(self, self.slugable_field))
        super(SlugableBehaviour, self).save(**kwargs)

    class Meta:
        abstract = True
