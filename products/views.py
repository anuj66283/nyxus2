from django.shortcuts import render
# from django.template import loader


# Create your views here.

def index(request):
    
    pdts= [
        {'img': 'static/images/1.jpeg', 'desc': 'dsfesgd fasz'},
        {'img': 'static/images/2.jpeg', 'desc': 'dsfesgd fasz'},
        {'img': 'static/images/1.jpeg', 'desc': 'dsfesgd fasz'},
        {'img': 'static/images/2.jpeg', 'desc': 'dsfesgd fasz'},
        {'img': 'static/images/1.jpeg', 'desc': 'dsfesgd fasz'}
    ]

    context = {
        "pdts": pdts
    }

    return render(request, 'index.html', context)