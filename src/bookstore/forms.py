from django import forms
from bookstore.models import Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class FullUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # fields = '__all__'
        fields = [
            'username',
            'email',
            'first_name',
            'last_name']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
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
