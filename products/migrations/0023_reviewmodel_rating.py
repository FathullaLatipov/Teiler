# Generated by Django 4.0.6 on 2022-07-26 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_reviewmodel_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewmodel',
            name='rating',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
    ]
