# Generated by Django 4.0.6 on 2022-10-25 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0112_alter_reviewmodel_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewmodel',
            name='review_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
