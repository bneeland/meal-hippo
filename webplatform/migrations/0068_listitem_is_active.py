# Generated by Django 3.0.4 on 2020-10-18 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webplatform', '0067_listitem_is_on_meal_hippo'),
    ]

    operations = [
        migrations.AddField(
            model_name='listitem',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]