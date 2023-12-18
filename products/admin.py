from django.contrib import admin
from .models import Product, Category

# Register your models here.
admin.site.register(Category)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created', 'updated')
