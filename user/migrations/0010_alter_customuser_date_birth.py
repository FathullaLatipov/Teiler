# Generated by Django 4.0.6 on 2022-08-07 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_alter_customuser_date_birth_alter_customuser_male'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
