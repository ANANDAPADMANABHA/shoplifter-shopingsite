# Generated by Django 3.2.13 on 2022-07-14 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cartapp', '0002_alter_cartitem_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='Cart',
            new_name='cart',
        ),
    ]
