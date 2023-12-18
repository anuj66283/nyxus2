from .models import Product, Category
from django.forms import ModelForm

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'price', 'description']

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']