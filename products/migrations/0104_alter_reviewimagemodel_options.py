# Generated by Django 4.0.6 on 2022-10-13 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0103_reviewimagemodel_remove_reviewmodel_image_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reviewimagemodel',
            options={'verbose_name': 'review_image', 'verbose_name_plural': 'reviews_image'},
        ),
    ]
