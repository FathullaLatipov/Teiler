# Generated by Django 4.0.6 on 2022-07-23 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_alter_productcharacteristicmodel_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewmodel',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='form_images', verbose_name='image'),
        ),
    ]
