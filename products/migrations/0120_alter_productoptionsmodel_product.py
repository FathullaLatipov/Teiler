# Generated by Django 4.0.6 on 2022-11-07 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0119_alter_productoptionsmodel_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productoptionsmodel',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products_options', to='products.productmodel', verbose_name='product'),
        ),
    ]
