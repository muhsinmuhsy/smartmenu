# Generated by Django 4.2.1 on 2023-07-04 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0034_cart_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='table',
        ),
    ]
