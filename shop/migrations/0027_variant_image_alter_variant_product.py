# Generated by Django 4.0.1 on 2022-08-29 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0026_color_size_remove_product_variant_variant'),
    ]

    operations = [
        migrations.AddField(
            model_name='variant',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='variant_images'),
        ),
        migrations.AlterField(
            model_name='variant',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variant', to='shop.product'),
        ),
    ]
