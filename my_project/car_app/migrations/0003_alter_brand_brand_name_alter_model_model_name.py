# Generated by Django 5.1.7 on 2025-03-26 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_app', '0002_alter_userprofile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='brand_name',
            field=models.CharField(max_length=34, unique=True),
        ),
        migrations.AlterField(
            model_name='model',
            name='model_name',
            field=models.CharField(max_length=34, unique=True),
        ),
    ]
