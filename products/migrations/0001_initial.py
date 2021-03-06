# Generated by Django 4.0.6 on 2022-07-09 17:21

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='title')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=300, verbose_name='title')),
                ('sku', models.IntegerField(db_index=True, verbose_name='sku')),
                ('brand', models.CharField(max_length=200, verbose_name='brand')),
                ('count', models.CharField(max_length=300, verbose_name='count')),
                ('price', models.IntegerField(verbose_name='price')),
                ('promotional_price', models.CharField(max_length=200, verbose_name='promotional_price')),
                ('inbox', models.CharField(max_length=300, verbose_name='inbox')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='description')),
                ('material', models.CharField(max_length=300, verbose_name='material')),
                ('country', models.CharField(max_length=300, verbose_name='country')),
                ('season', models.CharField(max_length=200, verbose_name='season')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.categorymodel', verbose_name='category')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
        ),
        migrations.CreateModel(
            name='ProductImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to='products', verbose_name='image')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='product', to='products.productmodel', verbose_name='product')),
            ],
            options={
                'verbose_name': 'product image',
                'verbose_name_plural': 'product images',
            },
        ),
    ]
