from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Product

# Create your views here.

def prdts(request):
    products = Product.objects.all()

    return render(request, "products.html", {'products': products})
    

def register(request):

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        print(form.errors.as_text())

        if form.is_valid():
            form.save()
            print("Form saved")
            return redirect("products")

    else:
        form = ProductForm()
    
    return render(request, "form.html", {'form': form})

def single(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, "single.html", {'product': product})


