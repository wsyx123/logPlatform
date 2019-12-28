# Generated by Django 2.1.14 on 2019-12-27 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminApp', '0012_auto_20191227_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logalarmrule',
            name='interval_time',
            field=models.IntegerField(blank=True, verbose_name='时间间隔'),
        ),
        migrations.AlterField(
            model_name='logalarmrule',
            name='total_number',
            field=models.IntegerField(blank=True, verbose_name='告警总次数'),
        ),
        migrations.AlterField(
            model_name='logalarmrule',
            name='total_time',
            field=models.IntegerField(blank=True, verbose_name='时间窗口'),
        ),
    ]