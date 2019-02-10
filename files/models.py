from django.db import models

from core.behaviours import (SlugableBehaviour, TimestampableBehaviour,
                             UUIDIndexBehaviour)
from core.mixins import SerializeMixin

from django.core.files.base import ContentFile

def update_config_file(instance, filename):
    return f'configurations/{instance.app.slug}/{filename}'

class ConfigFile(SlugableBehaviour, TimestampableBehaviour, UUIDIndexBehaviour, SerializeMixin, models.Model):

    name = models.CharField(max_length=30)
    filename = models.CharField(max_length=50)
    content = models.TextField()
    file = models.FileField(upload_to=update_config_file, blank=True, null=True, editable=False)

    app = models.ForeignKey('apps.App', on_delete=models.CASCADE, related_name="config_files")

    def save(self, *args, **kwargs):
        if self.file:
            self.file.delete(save=False)
        self.file.save(self.filename, ContentFile(self.content), save=False)
        super(ConfigFile, self).save(*args, **kwargs)