# Generated by Django 4.0.6 on 2022-10-02 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0077_colormodel_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='colormodel',
            old_name='title',
            new_name='color_title',
        ),
    ]
