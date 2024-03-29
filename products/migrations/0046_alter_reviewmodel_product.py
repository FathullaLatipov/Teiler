# Generated by Django 4.0.6 on 2022-08-17 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0045_alter_reviewmodel_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewmodel',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.productmodel', verbose_name='product'),
        ),
    ]
