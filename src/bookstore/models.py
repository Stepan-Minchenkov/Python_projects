from django.db import models
from datetime import date


# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(blank=True, null=True)
    price = models.DecimalField
    authors = models.ForeignKey('reference.Author', on_delete=models.PROTECT)
    series = models.ForeignKey('reference.Serie', on_delete=models.PROTECT)
    genre = models.ForeignKey('reference.Genre', on_delete=models.PROTECT)
    publish_year = models.DateField
    number_of_pages = models.IntegerField
    cover = models.CharField(max_length=20)
    book_format = models.CharField(max_length=20, blank=True, null=True)
    ISBN = models.CharField(max_length=30)
    weight = models.IntegerField
    allowed_age = models.IntegerField(blank=True, null=True)
    publisher = models.ForeignKey('reference.Publisher', on_delete=models.PROTECT)
    available = models.IntegerField
    active = models.BooleanField(default='Yes')
    rate = models.IntegerField(blank=True, null=True, default=0)
    created = models.DateField
    updated = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.name:20}  {self.authors:20}"


class GoodsInBasket(models.Model):
    order = models.CharField(max_length=100)
    article = models.ForeignKey(Book, on_delete=models.PROTECT)
    number = models.IntegerField
    created = models.DateField
    updated = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.order:20}  {self.article:20}  {self.created:20}  {self.updated:20}"


class Basket(models.Model):
    customer = models.CharField(max_length=100, default='Anonymous')
    goods = models.ForeignKey(GoodsInBasket, on_delete=models.PROTECT)
    created = models.DateField
    updated = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.customer:20}  {self.created:20}  {self.updated:20}"
