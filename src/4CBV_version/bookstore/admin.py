from django.contrib import admin

# Register your models here.
from . import models


class BasketAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created', 'updated')


class GoodsInBasket(admin.ModelAdmin):
    list_display = ('order', 'article', 'created', 'updated')


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'authors')


admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Basket, BasketAdmin)
admin.site.register(models.GoodsInBasket, GoodsInBasket)
