from django import forms


class LogeoForm(forms.Form):
    username = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'input'}))
