from django import forms
from . import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        # fields = '__all__'
        fields = [
            'name',
            'photo',
            'price',
            'authors',
            'series',
            'genre',
            'publish_year',
            'number_of_pages',
            'cover',
            'book_format',
            'ISBN',
            'weight',
            'allowed_age',
            'publisher',
            'available',
            'active',
            'rate']


class GoodsInBasketForm(forms.ModelForm):
    class Meta:
        model = models.GoodsInBasket
        # fields = '__all__'
        fields = [
            # 'order',
            # 'article',
            'quantity',
            # 'price',
            # 'total_sum'
        ]

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        if quantity <= 0:
            self.add_error('quantity', 'value must be positive')
        return cleaned_data


class BasketForm(forms.ModelForm):
    class Meta:
        model = models.Basket
        # fields = '__all__'
        fields = [
            # 'customer',
            'order_status',
            'contact_phone',
            'order_country',
            'order_city',
            'order_zip_code',
            'order_address1',
            'order_address2',
            'order_information']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if not self.request.user.is_authenticated:
            del self.fields['order_status']

        elif not self.request.user.has_perm("auth.manager") \
                and not self.request.user.has_perm("auth.admin"):
            del self.fields['order_status']

        basket_id = int(self.request.session.get('basket_pk', 0))
        if basket_id:
            basket = models.Basket.objects.get(pk=basket_id)
            if basket.customer:
                customer_data = models.Customer.objects.filter(user_data=basket.customer.id)
                if customer_data:
                    customer_data = models.Customer.objects.get(user_data=basket.customer.id)
                    self.initial['contact_phone'] = customer_data.phone
                    self.initial['order_country'] = customer_data.country
                    self.initial['order_city'] = customer_data.city
                    self.initial['order_zip_code'] = customer_data.zip_code
                    self.initial['order_address1'] = customer_data.address1
                    self.initial['order_address2'] = customer_data.address2
                    self.initial['order_information'] = customer_data.information


class BasketCommentsForm(forms.ModelForm):
    class Meta:
        model = models.BasketComments
        # fields = '__all__'
        fields = [
            'rate',
            'comment_text']


class BookCommentsForm(forms.ModelForm):
    class Meta:
        model = models.BookComments
        # fields = '__all__'
        fields = [
            'rate',
            'comment_text']
