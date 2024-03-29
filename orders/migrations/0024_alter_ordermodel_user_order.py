# Generated by Django 4.0.6 on 2022-08-22 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0023_remove_orderitem_user_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='user_order',
            field=models.CharField(blank=True, choices=[('process', 'В процессе'), ('cancel', 'Заказ отменен'), ('delivery', 'Выполняется доставка'), ('success', 'Товар получен')], default='process', max_length=200, null=True),
        ),
    ]
