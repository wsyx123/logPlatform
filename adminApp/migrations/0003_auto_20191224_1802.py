# Generated by Django 2.1.14 on 2019-12-24 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminApp', '0002_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
