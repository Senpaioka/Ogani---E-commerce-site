# Generated by Django 5.1.3 on 2025-02-01 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_blogcommentmodel_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogcommentmodel',
            name='count',
        ),
    ]
