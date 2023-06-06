from django import forms


class EmpoyeeForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.IntegerField()
    address = forms.CharField(widget=forms.Textarea)