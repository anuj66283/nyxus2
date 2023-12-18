from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm, CategoryForm
from .models import Product, Category

# Create your views here.

#read
def read_products(request):
    products = Product.objects.all()
    return render(request, "read_products.html", {'products': products})
    
#create
def create_products(request):

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            print("Form saved")
            return redirect("read_products")

    else:
        form = ProductForm()
    
    return render(request, "create_product.html", {'form': form})

#update
def update_product(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()

            return redirect("read_products")
        
    else:
        form = ProductForm(instance=product)

    return render(request, "create_product.html", {'form': form})

#delete

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method=='POST':
        product.delete()
        return redirect("read_products")
    
    return render(request, "delete_product.html", {'product': product})
    
###############################################3

#read
def read_category(request):
    category = Category.objects.all()
    return render(request, "read_category.html", {'category': category})
    
#create
def create_category(request):

    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("read_category")

    else:
        form = CategoryForm()
    
    return render(request, "create_product.html", {'form': form})

#update
def update_category(request, id):
    category = get_object_or_404(Category, pk=id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()

            return redirect("read_category")
        
    else:
        form = CategoryForm(instance=category)

    return render(request, "create_product.html", {'form': form})

#delete

def delete_category(request, id):
    category = get_object_or_404(Category, pk=id)

    if request.method=='POST':
        category.delete()
        return redirect("read_category")
    
    return render(request, "delete_product.html", {'product': category})
    

