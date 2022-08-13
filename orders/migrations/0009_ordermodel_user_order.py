# Generated by Django 4.0.6 on 2022-08-13 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_alter_ordermodel_upon_receipt'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='user_order',
            field=models.CharField(blank=True, choices=[('process', 'В процессе'), ('cancel', 'Заказ отменен'), ('delivery', 'Выполняется доставка'), ('success', 'Товар получен')], max_length=200, null=True),
        ),
    ]