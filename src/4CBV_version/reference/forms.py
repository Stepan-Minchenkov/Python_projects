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


class SerieForm(forms.ModelForm):
    class Meta:
        model = models.Serie
        fields = [
            'name',
            'description']


class GenreForm(forms.ModelForm):
    class Meta:
        model = models.Genre
        fields = [
            'name',
            'description']


class PublisherForm(forms.ModelForm):
    class Meta:
        model = models.Publisher
        fields = [
            'name',
            'description']
