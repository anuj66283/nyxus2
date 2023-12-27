from django.contrib import admin
from .models import Blog, CustomUser

# Register your models here.

@admin.register(CustomUser)
class AdminUser(admin.ModelAdmin):
    list_display =  ('id', 'username', 'email', 'password', 'verified')

@admin.register(Blog)
class AdminBlog(admin.ModelAdmin):
    list_display = ('id', 'title', 'created', 'updated', 'author')

# @admin.register(Comment)
# class AdminComment(admin.ModelAdmin):
#     list_display = ('id', 'body', 'author', 'post', 'created')