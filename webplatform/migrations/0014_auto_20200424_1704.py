# Generated by Django 3.0.4 on 2020-04-24 23:04

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webplatform', '0013_auto_20200424_1700'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserDeliveryDetails',
            new_name='UserDeliveryDetail',
        ),
    ]