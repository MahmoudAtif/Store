# Generated by Django 4.0.1 on 2022-08-29 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0029_product_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='color',
            name='code',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
