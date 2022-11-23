from django.contrib import admin

# Register your models here.
from . import models


class BasketAdmin(admin.ModelAdmin):
    list_display = ('pk', 'customer', 'order_status', 'created', 'updated')


class GoodsInBasketAdmin(admin.ModelAdmin):
    list_display = ('order', 'article', 'quantity', 'price', 'total_sum', 'created', 'updated')


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'authors', 'created', 'updated')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user_data', 'phone', 'country', 'city', 'zip_code', 'address1', 'address2')


admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Basket, BasketAdmin)
admin.site.register(models.GoodsInBasket, GoodsInBasketAdmin)
