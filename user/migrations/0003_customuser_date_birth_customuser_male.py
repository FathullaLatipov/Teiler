# Generated by Django 4.0.6 on 2022-08-04 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_customuser_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='Date_birth',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='date'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='male',
            field=models.CharField(max_length=20, null=True, verbose_name='male'),
        ),
    ]