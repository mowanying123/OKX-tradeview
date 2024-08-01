# Generated by Django 5.0 on 2024-07-31 19:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_photo', models.ImageField(upload_to='product_photos/')),
                ('product_description', models.TextField()),
                ('product_quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='vendingMachine.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='vendingMachine.user')),
            ],
        ),
    ]
