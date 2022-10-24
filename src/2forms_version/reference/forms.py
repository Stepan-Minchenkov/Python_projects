from django import forms


class AuthorForm(forms.Form):
    pk = forms.IntegerField(
        widget=forms.HiddenInput,
        required=False)
    name = forms.CharField(
        max_length=20,
        label="Author's name")
    surname = forms.CharField(
        max_length=20,
        label="Author's surname")
    description = forms.CharField(
        widget=forms.Textarea,
        required=False)

