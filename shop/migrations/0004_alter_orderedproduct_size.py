# Generated by Django 5.0.6 on 2024-06-17 22:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_orderedproduct_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderedproduct',
            name='size',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.size'),
        ),
    ]
