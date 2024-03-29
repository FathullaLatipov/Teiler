# Generated by Django 4.0.6 on 2022-08-02 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0029_rename_title_subcategorymodel_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategorymodel',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subcategories', to='products.categorymodel', verbose_name='category'),
        ),
    ]
