# Generated by Django 4.0.1 on 2022-08-20 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_alter_shopcart_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopcart',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
