# Generated by Django 2.1.2 on 2020-05-08 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ApiManager', '0002_testcaseinfo_is_complete'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('fail_num', models.IntegerField()),
                ('belong_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiManager.ProjectInfo')),
            ],
            options={
                'verbose_name': '用例执行结果',
                'db_table': 'TestResult',
            },
        ),
    ]