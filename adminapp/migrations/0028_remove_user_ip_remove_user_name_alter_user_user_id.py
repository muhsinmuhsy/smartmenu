# Generated by Django 4.2.1 on 2023-06-26 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0027_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='ip',
        ),
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.CharField(max_length=500),
        ),
    ]
