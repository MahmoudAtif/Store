# Generated by Django 4.1 on 2022-09-19 10:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0031_shopcart_variant'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-price']},
        ),
        migrations.AddField(
            model_name='product',
            name='wishlist',
            field=models.ManyToManyField(related_name='productFav', to=settings.AUTH_USER_MODEL),
        ),
    ]
