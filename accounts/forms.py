from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class signUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ("email","username", "password1", "password2")


class UserUpdateForm(forms.ModelForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'email')