# Generated by Django 4.0.6 on 2022-10-04 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0083_remove_productmodel_current_numbers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productmodel',
            old_name='colors',
            new_name='current_color',
        ),
    ]
