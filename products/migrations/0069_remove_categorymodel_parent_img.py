# Generated by Django 4.0.6 on 2022-09-30 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0068_categorymodel_parent_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorymodel',
            name='parent_img',
        ),
    ]
