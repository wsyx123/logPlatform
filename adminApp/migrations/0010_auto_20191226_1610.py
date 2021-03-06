# Generated by Django 2.1.14 on 2019-12-26 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminApp', '0009_logalarmexpression_rule'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logalarmrule',
            old_name='expression',
            new_name='logic_expression',
        ),
        migrations.AlterField(
            model_name='logalarmrule',
            name='enabled',
            field=models.BooleanField(default=False, verbose_name='生效'),
        ),
    ]
