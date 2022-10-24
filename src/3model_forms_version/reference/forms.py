from django import forms
from . import models


class AuthorForm(forms.ModelForm):
    class Meta:
        model = models.Author
        # fields = '__all__'
        fields = [
            'name',
            'surname',
            'description']


