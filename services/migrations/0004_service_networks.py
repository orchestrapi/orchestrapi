# Generated by Django 2.1.3 on 2019-01-31 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networks', '0003_auto_20190131_2040'),
        ('services', '0003_auto_20190109_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='networks',
            field=models.ManyToManyField(blank=True, null=True, related_name='services', to='networks.NetworkBridge'),
        ),
    ]
