# Generated by Django 5.1.3 on 2025-01-02 12:42

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_blogcategory_options_blogmodel_blog_thumb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogmodel',
            name='blog_body',
            field=ckeditor.fields.RichTextField(),
        ),
    ]