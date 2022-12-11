from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

STATUSES = [
    ('created', 'Created'),
    ('in_process', 'In Process'),
    ('done', 'Processed and delivered'),
    ('not_submitted', 'In doubt'),
    ('cancelled', 'Cancelled')
]

RATE = [(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'),
        (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'),  (10, '10')]


# Create your models here.
class Book(models.Model):
    name = models.CharField(_("name"), max_length=100)
    photo = models.ImageField(_("photo"), blank=True, null=True, upload_to='covers/%Y/%m/%d')
    price = models.DecimalField(_("price"), decimal_places=2, max_digits=5, validators=[MinValueValidator(0.0)])
    authors = models.ForeignKey('reference.Author', on_delete=models.PROTECT, related_name='books')
    series = models.ForeignKey('reference.Serie', on_delete=models.PROTECT, related_name='books',
                               blank=True, null=True)
    genre = models.ForeignKey('reference.Genre', on_delete=models.PROTECT, related_name='books')
    publish_year = models.CharField(_("publish_year"), max_length=4, default=datetime.now().date().year)
    number_of_pages = models.IntegerField(_("number_of_pages"), validators=[MinValueValidator(1)])
    cover = models.CharField(_("cover"), max_length=20)
    book_format = models.CharField(_("book_format"), max_length=20, blank=True, null=True, default='')
    ISBN = models.CharField(max_length=30)
    weight = models.IntegerField(_("weight"), validators=[MinValueValidator(1)])
    allowed_age = models.IntegerField(_("allowed_age"), blank=True, null=True, default=0)
    publisher = models.ForeignKey('reference.Publisher',
                                  on_delete=models.PROTECT, related_name='books')
    available = models.IntegerField(_("available"), validators=[MinValueValidator(0)])  ###???
    active = models.BooleanField(_("active"), default='Yes')
    rate = models.DecimalField(_("rate"), default=0, decimal_places=2, max_digits=4,
                               validators=[MinValueValidator(0.0)])
    created = models.DateField(_("created"), auto_now=False, auto_now_add=True)
    updated = models.DateField(_("updated"), auto_now=True, auto_now_add=False)

    def sortedcomments(self):
        all_comments = self.bookcomments.all().order_by("-created")
        return all_comments

    def averagerate(self):
        all_comments = self.bookcomments.all()
        # print(all_comments)
        rate = 0
        averagerate = 0
        if len(all_comments):
            for comment in all_comments:
                rate += comment.rate
            averagerate = rate/(len(all_comments))
        self.rate = averagerate
        self.save()
        return averagerate

    def __str__(self):
        return self.name

    # def __repr__(self):
    #     return f"{self.name:20}  {self.authors.name:20}"


User_min_data = get_user_model()


class Customer(models.Model):
    user_data = models.OneToOneField(User_min_data, on_delete=models.PROTECT, related_name='customers')
    phone = models.CharField(_("phone"), max_length=20)
    country = models.CharField(_("country"), max_length=20, blank=True, null=True)
    city = models.CharField(_("city"), max_length=20, blank=True, null=True)
    zip_code = models.CharField(_("zip_code"), max_length=20, blank=True, null=True)
    address1 = models.CharField(_("address1"), max_length=20, blank=True, null=True)
    address2 = models.CharField(_("address2"), max_length=20, blank=True, null=True)
    information = models.TextField(_("information"), blank=True, null=True)

    def __str__(self):
        return self.user_data.username

    # def __repr__(self):
    #     return f"{self.user_data.username:20} "

    def group_names(self):
        group_names = []
        for group in self.user_data.groups.all().values('name'):
            group_names.append(group['name'])
        return group_names


class Basket(models.Model):
    customer = models.ForeignKey(User_min_data, on_delete=models.PROTECT, related_name='baskets',
                                 blank=True, null=True)
    order_status = models.CharField(_("order_status"), max_length=20, choices=STATUSES, default='not_submitted')
    contact_phone = models.CharField(_("order_phone"), max_length=20, blank=True, null=True)
    order_country = models.CharField(_("order_country"), max_length=20, blank=True, null=True)
    order_city = models.CharField(_("order_city"), max_length=20, blank=True, null=True)
    order_zip_code = models.CharField(_("order_zip_code"), max_length=20, blank=True, null=True)
    order_address1 = models.CharField(_("order_address1"), max_length=20, blank=True, null=True)
    order_address2 = models.CharField(_("order_address2"), max_length=20, blank=True, null=True)
    order_information = models.TextField(_("order_information"), blank=True, null=True)
    created = models.DateField(_("created"), auto_now=False, auto_now_add=True)
    updated = models.DateField(_("updated"), auto_now=True, auto_now_add=False)

    def total_price(self):
        all_goods = self.goodsinbaskets.all()
        total_price = 0
        for goods in all_goods:
            total_price += goods.total_sum
        return total_price

    def total_books_number(self):
        all_goods = self.goodsinbaskets.all()
        total_books = 0
        for goods in all_goods:
            total_books += goods.quantity
        return total_books

    def sortedcomments(self):
        all_comments = self.basketcomments.all().order_by("-created")
        return all_comments

    def __str__(self):
        return str(self.pk)

    # def __repr__(self):
    #     return f"{self.customer.username:20}  {self.created:20}  {self.updated:20}"


class GoodsInBasket(models.Model):
    order = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='goodsinbaskets')
    article = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='goodsinbaskets')
    quantity = models.IntegerField(_("quantity"), validators=[MinValueValidator(1)])
    price = models.DecimalField(_("price"), decimal_places=2, max_digits=5, validators=[MinValueValidator(0.0)])
    total_sum = models.DecimalField(_("total_sum"), decimal_places=2, max_digits=6, validators=[MinValueValidator(0.0)])
    created = models.DateField(_("created"), auto_now=False, auto_now_add=True)
    updated = models.DateField(_("updated"), auto_now=True, auto_now_add=False)

    def __str__(self):
        return str(self.order.pk)

    # def __repr__(self):
    #     return f"{self.order:20}  {self.article.name:20}  {self.created:20}  {self.updated:20}"


class BasketComments(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='basketcomments')
    customer = models.ForeignKey(User_min_data, on_delete=models.PROTECT, related_name='basketcomments')
    comment_text = models.TextField(_("comment_text"))
    rate = models.IntegerField(_("rate"), choices=RATE, blank=True, null=True,
                               validators=[MinValueValidator(0), MaxValueValidator(10)])
    created = models.DateField(_("created"), auto_now=False, auto_now_add=True)
    updated = models.DateField(_("updated"), auto_now=True, auto_now_add=False)

    def __str__(self):
        return str(self.pk)


class BookComments(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='bookcomments')
    customer = models.ForeignKey(User_min_data, on_delete=models.PROTECT, related_name='bookcomments')
    comment_text = models.TextField(_("comment_text"))
    rate = models.IntegerField(_("rate"), default=10, choices=RATE,
                               validators=[MinValueValidator(0), MaxValueValidator(10)])
    created = models.DateField(_("created"), auto_now=False, auto_now_add=True)
    updated = models.DateField(_("updated"), auto_now=True, auto_now_add=False)

    def __str__(self):
        return str(self.pk)
