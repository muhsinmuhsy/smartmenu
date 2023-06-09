# Generated by Django 4.2.1 on 2023-06-06 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(null=True, upload_to='product_image')),
                ('description', models.CharField(max_length=100)),
                ('availability', models.BooleanField(default=False)),
                ('category', models.ManyToManyField(to='adminapp.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('actual_price', models.IntegerField()),
                ('discount_price', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.product')),
            ],
        ),
    ]
