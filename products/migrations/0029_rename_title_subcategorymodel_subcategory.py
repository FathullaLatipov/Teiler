# Generated by Django 4.0.6 on 2022-08-02 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0028_rename_subcategory_subcategorymodel_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subcategorymodel',
            old_name='title',
            new_name='subcategory',
        ),
    ]