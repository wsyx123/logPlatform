# Generated by Django 2.1.14 on 2019-12-27 11:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adminApp', '0010_auto_20191226_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='logalarmrule',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='logalarmrule',
            unique_together={('name', 'business')},
        ),
    ]
