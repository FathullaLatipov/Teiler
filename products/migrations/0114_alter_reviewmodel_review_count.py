# Generated by Django 4.0.6 on 2022-10-25 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0113_reviewmodel_review_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewmodel',
            name='review_count',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
