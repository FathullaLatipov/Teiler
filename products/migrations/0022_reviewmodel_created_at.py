# Generated by Django 4.0.6 on 2022-07-23 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_reviewmodel_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewmodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='created_at'),
        ),
    ]
