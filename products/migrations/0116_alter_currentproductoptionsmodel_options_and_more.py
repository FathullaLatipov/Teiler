# Generated by Django 4.0.6 on 2022-10-28 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0115_currentproductoptionsmodel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currentproductoptionsmodel',
            options={'ordering': ['pk'], 'verbose_name': 'Current_product_options', 'verbose_name_plural': 'Current_product_options'},
        ),
        migrations.RenameField(
            model_name='currentproductoptionsmodel',
            old_name='options_number',
            new_name='current_options_number',
        ),
        migrations.RenameField(
            model_name='currentproductoptionsmodel',
            old_name='options_title',
            new_name='current_options_title',
        ),
    ]
