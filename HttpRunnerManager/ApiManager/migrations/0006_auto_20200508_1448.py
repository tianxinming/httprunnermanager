# Generated by Django 2.1.2 on 2020-05-08 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApiManager', '0005_auto_20200508_1432'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testresult',
            name='id',
        ),
        migrations.AlterField(
            model_name='testresult',
            name='belong_project',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, unique=True, verbose_name='所属项目'),
        ),
    ]
