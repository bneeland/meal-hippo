# Generated by Django 3.0.4 on 2020-05-02 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webplatform', '0029_auto_20200501_0740'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='minimum_lead_time',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='supplier',
            name='minimum_portions',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
