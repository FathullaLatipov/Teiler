# Generated by Django 4.0.6 on 2022-10-01 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0071_alter_productmodel_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='status',
            field=models.CharField(blank=True, choices=[('PROCESS', 'В процессе'), ('CANCELED', 'Отменен'), ('WAIT_SEND', 'Ожидает доставка'), ('WAIT_REV', 'Ожидает отзыв'), ('COMPLETE', 'Товар получен')], default='PROCESS', max_length=200, null=True),
        ),
    ]
