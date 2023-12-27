from .models import Blog, CustomUser
from django.forms import ModelForm
from django import forms

class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'body']

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("email already exists")
    
        return email


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        password1 = cleaned_data['password1']

        if password != password1:
            raise forms.ValidationError("Cannot verify password")
    
        return cleaned_data
    


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
