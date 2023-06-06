from django import forms
from .models import UserModel


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'email', 'phone', 'address', 'password', 'document', )