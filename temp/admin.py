from django.contrib import admin
from . import models

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio')

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'list_genre', 'list_author')
    search_fields = ('title',)

    def list_genre(self, obj):
        return ', '.join([x.name for x in obj.category.all()])
    
    list_genre.short_description = "Genre"

    def list_author(self, obj):
        return obj.author.name
    
    list_author.short_description = "Author"

    
    

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Register your models here.
admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Category, CategoryAdmin)
