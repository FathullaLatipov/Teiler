# Generated by Django 4.0.6 on 2022-09-30 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0065_remove_subcategorymodel_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorymodel',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='products.categorymodel'),
        ),
    ]
