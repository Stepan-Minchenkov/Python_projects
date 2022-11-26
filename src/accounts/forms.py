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
    phone = forms.CharField(label="Phone", widget=forms.TextInput(), max_length=20, required=False)

    class Meta:
        model = User
        # fields = '__all__'
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     user = User.objects.get(username=self.instance.username)
    #     customer = Customer.objects.get(user_data=user.id)
    #     print(Customer.objects.filter(user_data=user.id).values('phone'))
    #     print(self.fields['phone'].get_bound_field(self, 'phone'))
    #     # self.fields['phone'].value  = Customer.objects.filter(user_data=user.id).values('phone')
    #     self.fields['phone'].value = customer.phone
    #     self.fields['first_name'].value = "DFFFF"
    #     # self.fields['first_name'].queryset = 'DFFFF'
    #     print(self.fields)
    #     print(self.fields['phone'].get_bound_field(self, 'phone'))
    #     print(self.fields['phone'].get_bound_field(self, 'first_name'))


class ChangeCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        # fields = '__all__'
        fields = [
            'phone', ]
