from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.signals import pre_delete, post_save

from core.behaviours import (SlugableBehaviour, TimestampableBehaviour,
                             UUIDIndexBehaviour)
from core.mixins import SerializeMixin


def update_config_file(instance, filename):
    if instance.app:
        return f'configurations/{instance.app.slug}/{filename}'
    return f'configurations/{instance.service.slug}/{filename}'


class ConfigFile(SlugableBehaviour, TimestampableBehaviour, UUIDIndexBehaviour, SerializeMixin, models.Model):

    name = models.CharField(max_length=30)
    filename = models.CharField(max_length=50)
    content = models.TextField()
    file = models.FileField(upload_to=update_config_file,
                            blank=True, null=True)

    app = models.ForeignKey('apps.App', on_delete=models.CASCADE,
                            related_name="config_files", blank=True, null=True)
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE,
                                related_name="config_files", blank=True, null=True)

    def clean(self):
        if not self.app and not self.service:
            raise ValidationError("no hay ni servicio ni app asociada")
        if self.app and self.service:
            raise ValidationError(
                "No puede estar asociado a un servicio y una app")

    def save(self, *args, **kwargs):
        prevent_default = kwargs.pop('prevent_default_save', None)
        if not prevent_default:
            self.clean()
            if self.file:
                self.file.delete(save=False)
            self.file.save(self.filename, ContentFile(self.content), save=False)
            super(ConfigFile, self).save(*args, **kwargs)

    def update_container_ips(self, app):
        template = self.content
        containers = app.running_containers_ips_and_port
        template = template.replace('${container-addrs}', ','.join(containers))
        if self.file:
            self.file.delete(save=False)
        self.file.save(self.filename, ContentFile(template), save=False)
        self.save(prevent_default_save=True)


# SIGNALS

def remove_files_from_system(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)

def restart_service_if_main_file_changes(sender, instance, **kwargs):
    if not instance.service.data.get('main_config_file') == instance.slug:
        return
    for app in instance.service.apps.all():
        instance.update_container_ips(app)
        
    instance.service.dclient.get_container_by_name(instance.service.container_id).restart()

pre_delete.connect(remove_files_from_system, sender=ConfigFile)
post_save.connect(restart_service_if_main_file_changes, sender=ConfigFile)
