# Generated by Django 4.0.6 on 2022-07-31 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_alter_reviewmodel_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisterForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('phone', models.PositiveSmallIntegerField()),
                ('password', models.CharField(max_length=100, null=True)),
                ('confirm_password', models.CharField(max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'register',
                'verbose_name_plural': 'registers',
            },
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]