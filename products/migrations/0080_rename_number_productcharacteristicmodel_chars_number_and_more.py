# Generated by Django 4.0.6 on 2022-10-02 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0079_rename_custom_number_productcustomnamemodel_chars_number_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productcharacteristicmodel',
            old_name='number',
            new_name='chars_number',
        ),
        migrations.RenameField(
            model_name='productcharacteristicmodel',
            old_name='data',
            new_name='chars_title',
        ),
    ]
