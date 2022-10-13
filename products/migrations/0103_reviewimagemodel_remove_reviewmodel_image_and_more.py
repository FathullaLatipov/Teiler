# Generated by Django 4.0.6 on 2022-10-13 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0102_reviewmodel_review_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='form_images', verbose_name='image')),
            ],
            options={
                'verbose_name': 'review',
                'verbose_name_plural': 'reviews',
            },
        ),
        migrations.RemoveField(
            model_name='reviewmodel',
            name='image',
        ),
        migrations.AddField(
            model_name='reviewmodel',
            name='image',
            field=models.ManyToManyField(to='products.reviewimagemodel'),
        ),
    ]