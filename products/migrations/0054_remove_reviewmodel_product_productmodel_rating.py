# Generated by Django 4.0.6 on 2022-09-11 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0053_productcustommodel_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewmodel',
            name='product',
        ),
        migrations.AddField(
            model_name='productmodel',
            name='rating',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='products.reviewmodel'),
            preserve_default=False,
        ),
    ]
