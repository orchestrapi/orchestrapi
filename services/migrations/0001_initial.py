# Generated by Django 5.1.4 on 2025-01-10 14:37

import core.mixins
import services.mixins
import services.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('networks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('container_id', models.CharField(blank=True, max_length=20, null=True)),
                ('name', models.CharField(max_length=30)),
                ('params', models.JSONField(blank=True, default=dict)),
                ('data', models.JSONField(blank=True, default=services.models.default_data)),
                ('networks', models.ManyToManyField(blank=True, related_name='services', to='networks.networkbridge')),
            ],
            options={
                'abstract': False,
            },
            bases=(core.mixins.SerializeMixin, services.mixins.LoadBalancerMixin, models.Model),
        ),
    ]
