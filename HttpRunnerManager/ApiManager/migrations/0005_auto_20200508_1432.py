# Generated by Django 2.1.2 on 2020-05-08 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApiManager', '0004_auto_20200508_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testresult',
            name='fail_num',
            field=models.IntegerField(),
        ),
    ]