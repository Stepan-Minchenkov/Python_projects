from django.db import models
from datetime import date
from django.contrib.auth import get_user_model

# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(blank=True, null=True)
    price = models.DecimalField
    authors = models.ForeignKey('reference.Author', on_delete=models.PROTECT, related_name='book')
    series = models.ForeignKey('reference.Serie', on_delete=models.PROTECT, related_name='book')
    genre = models.ForeignKey('reference.Genre', on_delete=models.PROTECT, related_name='book')
    publish_year = models.DateField
    number_of_pages = models.IntegerField
    cover = models.CharField(max_length=20)
    book_format = models.CharField(max_length=20, blank=True, null=True, default='')
    ISBN = models.CharField(max_length=30)
    weight = models.IntegerField
    allowed_age = models.IntegerField(blank=True, null=True, default=0)
    publisher = models.ForeignKey('reference.Publisher', on_delete=models.PROTECT, related_name='book')
    available = models.IntegerField
    active = models.BooleanField(default='Yes')
    rate = models.IntegerField(blank=True, null=True, default=0)
    created = models.DateField
    updated = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.name:20}  {self.authors:20}"

    def __repr__(self):
        return self.name


class GoodsInBasket(models.Model):
    order = models.CharField(max_length=100)
    article = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='goodsinbasket')
    number = models.IntegerField
    created = models.DateField
    updated = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.order:20}  {self.article:20}  {self.created:20}  {self.updated:20}"

    def __repr__(self):
        return self.order


class Basket(models.Model):
    customer = models.CharField(max_length=100, default='Anonymous')
    goods = models.ForeignKey(GoodsInBasket, on_delete=models.PROTECT, related_name='basket')
    created = models.DateField
    updated = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.customer:20}  {self.created:20}  {self.updated:20}"

    def __repr__(self):
        return self.customer


User = get_user_model()

# class Customer(models.Model):
#     User_data = models.OneToOneField(User, on_delete=models.PROTECT, related_name='customer')
#     phone = models.CharField(max_length=20)
#     country = models.CharField(max_length=20)
#     city = models.CharField(max_length=20)
#     zip_code = models.CharField(max_length=20)
#     address1 = models.CharField(max_length=20)
#     address2 = models.CharField(max_length=20)
#     information = models.TextField(blank=True, null=True)
#
#     def __str__(self):
#         return f"{self.logon:20}  {self.name:20}  {self.surname:20}"

#     def __repr__(self):
#         return self.name
# from django.contrib.auth.models import User, Group
# Group.objects.name = "Customers"
