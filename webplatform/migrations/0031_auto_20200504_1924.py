# Generated by Django 3.0.4 on 2020-05-05 01:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webplatform', '0030_auto_20200502_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplier',
            name='minimum_lead_time',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='minimum_portions',
        ),
    ]
