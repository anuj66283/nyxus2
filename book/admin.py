from django.contrib import admin
from .models import Books, Cart, Checkout


# Register your models here.
@admin.register(Books)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "genre", "price", "desc")

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user")

@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "address")