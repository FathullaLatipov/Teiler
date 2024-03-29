# Generated by Django 4.0.6 on 2022-08-10 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='online',
            field=models.CharField(blank=True, choices=[('Картой онлайн', 'Картой онлайн'), ('Оплата при получении', 'Оплата при получении')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='upon_receipt',
            field=models.CharField(blank=True, choices=[('Получить почтой', 'Получить почтой'), ('Доставить курьером', 'Доставить курьером'), ('Получить из почтамата', 'Получить из почтамата')], max_length=100, null=True),
        ),
    ]
