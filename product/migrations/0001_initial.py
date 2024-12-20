# Generated by Django 5.1.3 on 2024-12-03 16:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('product_category', models.CharField(choices=[('category', 'category')], max_length=10)),
                ('category_image', models.ImageField(blank=True, upload_to='category/photos')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Product Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('product_info', models.CharField(blank=True, max_length=255)),
                ('product_description', models.TextField(blank=True)),
                ('product_price', models.FloatField()),
                ('product_image', models.ImageField(upload_to='product/photos')),
                ('product_thumb', models.ImageField(upload_to='product/thumbnails')),
                ('product_weight', models.FloatField()),
                ('shipping', models.CharField(max_length=100)),
                ('is_available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('product_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.productcategory')),
            ],
        ),
    ]
