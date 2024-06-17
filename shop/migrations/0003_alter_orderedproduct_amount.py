# Generated by Django 5.0.6 on 2024-06-17 21:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_order_processed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderedproduct',
            name='amount',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
