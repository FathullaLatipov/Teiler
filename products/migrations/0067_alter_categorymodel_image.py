# Generated by Django 4.0.6 on 2022-09-30 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0066_alter_categorymodel_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorymodel',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='image', verbose_name='image'),
        ),
    ]