# Generated by Django 4.1.2 on 2022-11-20 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0010_alter_book_series'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publish_year',
            field=models.CharField(default=2022, max_length=4),
        ),
    ]
