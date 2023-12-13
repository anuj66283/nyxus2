from django.shortcuts import render
from . import models

# Create your views here.

def display(request):
    bk = models.Book.objects.all()
    au = models.Author.objects.all()

    context = {
        'au': au,
        'bk': bk
    }

    return render(request, 'main.html', context)