# Generated by Django 5.1.3 on 2025-02-01 06:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_alter_blogcommenttracker_comment_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcommenttracker',
            name='blog',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.blogmodel'),
        ),
    ]
