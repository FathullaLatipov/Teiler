# Generated by Django 4.0.6 on 2022-09-30 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0067_alter_categorymodel_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorymodel',
            name='parent_img',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cat_images', to='products.categorymodel'),
        ),
    ]