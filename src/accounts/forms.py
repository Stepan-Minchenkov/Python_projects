from django import forms
from bookstore.models import Customer
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


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        # fields = '__all__'
        fields = [
            'phone',
            'country',
            'city',
            'zip_code',
            'address1',
            'address2',
            'information']


class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = '__all__'
        fields = [
            'email',
            'first_name',
            'last_name']


class ChangeCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        # fields = '__all__'
        fields = [
            'phone',]
