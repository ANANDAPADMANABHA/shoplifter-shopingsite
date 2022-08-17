# Generated by Django 3.2.13 on 2022-07-31 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartapp', '0006_alter_cartitem_cartprice'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(blank=True, max_length=10)),
                ('discount', models.FloatField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
