# Generated by Django 3.0.4 on 2020-04-25 04:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webplatform', '0021_auto_20200424_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_time',
            field=models.TimeField(blank=True, default=datetime.time(22, 12, 42, 496651), null=True),
        ),
    ]
