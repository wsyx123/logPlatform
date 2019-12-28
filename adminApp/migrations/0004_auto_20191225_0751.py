# Generated by Django 2.1.14 on 2019-12-25 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminApp', '0003_auto_20191224_1802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logalarmrule',
            name='businessID',
        ),
        migrations.AddField(
            model_name='logalarmrule',
            name='business',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='adminApp.Business', verbose_name='所属业务'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='logalarmrule',
            name='level',
            field=models.IntegerField(choices=[(1, '低'), (2, '中'), (3, '高')], verbose_name='告警级别'),
        ),
    ]
