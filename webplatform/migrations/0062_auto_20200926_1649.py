# Generated by Django 3.0.4 on 2020-09-26 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webplatform', '0061_day_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='day',
            old_name='name',
            new_name='name_full',
        ),
        migrations.AddField(
            model_name='day',
            name='name_short',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
