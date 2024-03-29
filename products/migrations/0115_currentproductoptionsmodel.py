# Generated by Django 4.0.6 on 2022-10-28 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0114_alter_reviewmodel_review_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentProductOptionsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('options_title', models.CharField(max_length=300, verbose_name='options_title')),
                ('options_number', models.CharField(max_length=300, verbose_name='options_number')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='current_products_options', to='products.productmodel', verbose_name='product')),
            ],
            options={
                'verbose_name': 'product_options',
                'verbose_name_plural': 'product_options',
            },
        ),
    ]
