# Generated by Django 4.0.1 on 2022-08-20 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_alter_comment_comment_alter_comment_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='subject',
        ),
    ]
