# Generated by Django 2.1.2 on 2018-10-28 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_project_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='file_path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]