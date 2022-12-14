# Generated by Django 4.1.1 on 2022-10-20 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reference', '0002_alter_author_description_alter_genre_name_and_more'),
        ('bookstore', '0002_basket_updated_book_updated_goodsinbasket_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='basket', to='bookstore.goodsinbasket'),
        ),
        migrations.AlterField(
            model_name='book',
            name='authors',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='book', to='reference.author'),
        ),
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='book', to='reference.genre'),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='book', to='reference.publisher'),
        ),
        migrations.AlterField(
            model_name='book',
            name='series',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='book', to='reference.serie'),
        ),
        migrations.AlterField(
            model_name='goodsinbasket',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='goodsinbasket', to='bookstore.book'),
        ),
    ]
