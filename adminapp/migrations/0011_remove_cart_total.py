# Generated by Django 4.2.1 on 2023-06-14 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0010_alter_cart_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='total',
        ),
    ]
