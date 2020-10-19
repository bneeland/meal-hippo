# Generated by Django 3.0.4 on 2020-10-17 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webplatform', '0065_listitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listitem',
            name='menu',
        ),
        migrations.AddField(
            model_name='listitem',
            name='delivery_details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='listitem',
            name='how_to_order_details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='listitem',
            name='menu_items',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='listitem',
            name='menu_prices',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='listitem',
            name='payment_process_details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='listitem',
            name='pickup_details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='listitem',
            name='food_format',
            field=models.TextField(blank=True, null=True),
        ),
    ]