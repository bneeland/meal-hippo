# Generated by Django 3.0.4 on 2020-09-20 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webplatform', '0055_auto_20200920_1752'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersupplierinfo',
            name='is_supplier',
        ),
        migrations.AddField(
            model_name='usersupplierinfo',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
