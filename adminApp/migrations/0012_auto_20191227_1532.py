# Generated by Django 2.1.14 on 2019-12-27 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminApp', '0011_auto_20191227_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='logalarmrule',
            name='component',
            field=models.IntegerField(blank=True, default=1, verbose_name='组件ID'),
            preserve_default=False,
        ),
    ]