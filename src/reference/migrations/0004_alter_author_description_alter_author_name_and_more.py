# Generated by Django 4.1.2 on 2022-11-27 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reference', '0003_alter_genre_description_alter_publisher_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='description',
            field=models.TextField(blank=True, default='', null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=20, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='author',
            name='surname',
            field=models.CharField(max_length=20, verbose_name='surname'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='description',
            field=models.TextField(blank=True, default='', null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=20, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='description',
            field=models.TextField(blank=True, default='', null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='serie',
            name='description',
            field=models.TextField(blank=True, default='', null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='serie',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='name'),
        ),
    ]
