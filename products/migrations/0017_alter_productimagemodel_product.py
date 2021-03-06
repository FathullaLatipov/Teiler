# Generated by Django 4.0.6 on 2022-07-20 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_alter_rating_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimagemodel',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='images', to='products.productmodel', verbose_name='product'),
        ),
    ]
