# Generated by Django 4.0.1 on 2022-08-29 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0028_remove_product_minamount'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
