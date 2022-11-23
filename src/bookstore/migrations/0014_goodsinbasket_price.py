# Generated by Django 4.1.2 on 2022-11-22 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0013_remove_basket_goods_basket_contact_phone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodsinbasket',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
    ]
