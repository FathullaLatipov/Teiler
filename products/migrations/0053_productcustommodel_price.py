# Generated by Django 4.0.6 on 2022-08-31 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0052_productattributes'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcustommodel',
            name='price',
            field=models.PositiveIntegerField(null=True, verbose_name='price'),
        ),
    ]
