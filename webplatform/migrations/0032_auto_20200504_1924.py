# Generated by Django 3.0.4 on 2020-05-05 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webplatform', '0031_auto_20200504_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='minimum_lead_time',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='minimum_portions',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]