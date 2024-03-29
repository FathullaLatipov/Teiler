# Generated by Django 4.0.6 on 2022-10-01 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0074_productmodel_is_fav'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewmodel',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rating', to='products.productmodel', verbose_name='product'),
        ),
    ]
