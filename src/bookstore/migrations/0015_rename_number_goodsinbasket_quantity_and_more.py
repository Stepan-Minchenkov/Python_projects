# Generated by Django 4.1.2 on 2022-11-22 13:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookstore', '0014_goodsinbasket_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goodsinbasket',
            old_name='number',
            new_name='quantity',
        ),
        migrations.AlterField(
            model_name='basket',
            name='customer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='basket', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='basket',
            name='order_address1',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='basket',
            name='order_address2',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='basket',
            name='order_city',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='basket',
            name='order_country',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='basket',
            name='order_status',
            field=models.CharField(choices=[('created', 'Created'), ('in_process', 'In Process'), ('done', 'Processed and delivered'), ('', 'In doubt')], default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='basket',
            name='order_zip_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]