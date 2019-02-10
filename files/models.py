from django.db import models

from core.behaviours import (SlugableBehaviour, TimestampableBehaviour,
                             UUIDIndexBehaviour)
from core.mixins import SerializeMixin

from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError

def update_config_file(instance, filename):
    if instance.app:
        return f'configurations/{instance.app.slug}/{filename}'
    return f'configurations/{instance.service.slug}/{filename}'

class ConfigFile(SlugableBehaviour, TimestampableBehaviour, UUIDIndexBehaviour, SerializeMixin, models.Model):

    name = models.CharField(max_length=30)
    filename = models.CharField(max_length=50)
    content = models.TextField()
    file = models.FileField(upload_to=update_config_file, blank=True, null=True, editable=False)

    app = models.ForeignKey('apps.App', on_delete=models.CASCADE, related_name="config_files", blank=True, null=True)
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE, related_name="config_files", blank=True, null=True)

    def clean(self):
        if not self.app and not self.service:
            raise ValidationError("no hay ni servicio ni app asociada")
        if self.app and self.service:
            raise ValidationError("No puede estar asociado a un servicio y una app")

    def save(self, *args, **kwargs):
        self.clean()
        if self.file:
            self.file.delete(save=False)
        self.file.save(self.filename, ContentFile(self.content), save=False)
        super(ConfigFile, self).save(*args, **kwargs)