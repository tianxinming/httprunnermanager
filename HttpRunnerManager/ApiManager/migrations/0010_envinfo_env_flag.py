# Generated by Django 2.0.3 on 2020-05-11 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApiManager', '0009_moduleinfo_mode_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='envinfo',
            name='env_flag',
            field=models.CharField(default='test', max_length=40, null=True),
        ),
    ]