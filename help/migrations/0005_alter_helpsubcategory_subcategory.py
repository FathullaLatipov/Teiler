# Generated by Django 4.0.6 on 2022-07-16 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0004_helpmodel_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helpsubcategory',
            name='subcategory',
            field=models.CharField(db_index=True, max_length=200, null=True, verbose_name='subcategory'),
        ),
    ]
