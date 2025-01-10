# Generated by Django 5.1.3 on 2025-01-10 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactInfoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=100)),
                ('open_time', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
