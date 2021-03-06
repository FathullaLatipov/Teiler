# Generated by Django 4.0.6 on 2022-07-16 17:43

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HelpCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
            ],
            options={
                'verbose_name': 'help_category',
                'verbose_name_plural': 'help_categories',
            },
        ),
        migrations.CreateModel(
            name='HelpSubcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='help.helpcategory', verbose_name='category')),
            ],
            options={
                'verbose_name': 'Help_subcategory',
                'verbose_name_plural': 'Help_subcategories',
            },
        ),
        migrations.CreateModel(
            name='HelpModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('descriptions', ckeditor_uploader.fields.RichTextUploadingField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='help.helpcategory', verbose_name='category')),
            ],
            options={
                'verbose_name': 'Help_model',
                'verbose_name_plural': 'Help_models',
            },
        ),
    ]
