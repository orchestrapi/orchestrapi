# Generated by Django 5.1.4 on 2025-01-10 14:37

import core.mixins
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NetworkBridge',
            fields=[
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('network_id', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(core.mixins.SerializeMixin, models.Model),
        ),
    ]
