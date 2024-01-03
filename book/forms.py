from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Checkout, Reviews

class UserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=60)
    password = forms.CharField(max_length=60, widget=forms.PasswordInput)

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = ("address",)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ("review", "rating")