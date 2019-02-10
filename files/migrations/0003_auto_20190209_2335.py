# Generated by Django 2.1.3 on 2019-02-09 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_auto_20190209_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='configfile',
            name='content',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configfile',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='config_files/'),
        ),
        migrations.AddField(
            model_name='configfile',
            name='filename',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configfile',
            name='name',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
