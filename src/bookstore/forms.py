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
