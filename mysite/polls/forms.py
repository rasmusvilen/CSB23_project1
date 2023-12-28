from django import forms
from .models import UserAccount

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserAccount
        fields = ['username', 'password']