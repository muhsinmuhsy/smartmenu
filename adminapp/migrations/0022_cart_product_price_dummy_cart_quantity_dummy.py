# Generated by Django 4.2.1 on 2023-06-14 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0021_alter_cart_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='product_price_dummy',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='quantity_dummy',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
