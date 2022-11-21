# Generated by Django 4.1.2 on 2022-11-20 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0008_basket_created_book_available_book_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='basket',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='goodsinbasket',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='goodsinbasket',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
    ]