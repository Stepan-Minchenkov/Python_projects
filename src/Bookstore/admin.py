from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Book)
admin.site.register(models.Basket)
admin.site.register(models.GoodsInBasket)
