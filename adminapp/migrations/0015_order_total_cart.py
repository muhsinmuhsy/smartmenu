# Generated by Django 4.2.1 on 2023-06-14 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0014_alter_cart_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_cart',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]