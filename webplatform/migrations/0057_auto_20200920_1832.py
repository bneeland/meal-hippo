# Generated by Django 3.0.4 on 2020-09-21 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webplatform', '0056_auto_20200920_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersupplierinfo',
            name='agree_to_terms_conditions',
            field=models.BooleanField(default=False, verbose_name='I agree to the Meal Hippo General Terms and Conditions for Services &ndash; Caterers&mdash;as amended from time to time.'),
        ),
    ]
