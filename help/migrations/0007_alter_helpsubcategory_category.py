# Generated by Django 4.0.6 on 2022-07-16 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0006_alter_helpsubcategory_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helpsubcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='help_subcategories', to='help.helpcategory', verbose_name='category'),
        ),
    ]
