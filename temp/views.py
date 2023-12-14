from django.shortcuts import render, HttpResponse
from . import models

# Create your views here.

def book(request):


    bks = models.Book.objects.select_related('author').all()

    context = {
        'books': bks
    }

    return render(request, 'index.html', context)
