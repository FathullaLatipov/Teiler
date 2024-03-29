# Generated by Django 4.0.6 on 2022-10-01 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0070_productmodel_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='status',
            field=models.CharField(blank=True, choices=[('process', 'В процессе'), ('cancel', 'Отменен'), ('wait_send', 'Ожидает доставка'), ('wait_rev', 'Ожидает отзыв'), ('success', 'Товар получен')], default='process', max_length=200, null=True),
        ),
    ]
