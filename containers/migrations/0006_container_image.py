# Generated by Django 2.1.2 on 2018-10-31 23:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_image_local_build'),
        ('containers', '0005_auto_20181101_0006'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='containers', to='images.Image'),
        ),
    ]
