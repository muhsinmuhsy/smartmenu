# Generated by Django 4.2.1 on 2023-06-14 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0009_cart_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
