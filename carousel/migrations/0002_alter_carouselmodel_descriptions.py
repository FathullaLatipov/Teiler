# Generated by Django 4.0.6 on 2022-09-12 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carousel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carouselmodel',
            name='descriptions',
            field=models.TextField(verbose_name='descriptions'),
        ),
    ]
