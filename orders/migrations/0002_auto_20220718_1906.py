# Generated by Django 3.2.13 on 2022-07-18 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cartapp', '0004_cartitem_user'),
        ('accounts', '0009_auto_20220715_1221'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='carts',
            field=models.ManyToManyField(null=True, to='cartapp.CartItem'),
        ),
        migrations.RemoveField(
            model_name='orders',
            name='address',
        ),
        migrations.AddField(
            model_name='orders',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.address'),
        ),
    ]
