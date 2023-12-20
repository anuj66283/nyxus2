from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog
from .forms import BlogForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == "POST":

        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            login(request, user)

            return redirect("view_all")
    
    else:
        form = UserCreationForm()
    
    return render(request, "signup.html", {'form': form})

def signout(request):
    logout(request)
    return redirect('view_all')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        
        if user is not None:
            print(user)
            login(request, user)
            return redirect("view_all")
    
    return render(request, "login.html")

@login_required
def create_blog(request):
    if request.method=="POST":
        form = BlogForm(request.POST)

        if form.is_valid():
            temp = form.save(commit=False)
            temp.author = request.user
            temp.save()
            return redirect("view_all")
    
    else:
        form = BlogForm()
    
    return render(request, "create_blog.html", {"form": form})

@login_required
def update_blog(request, id):
    blog = get_object_or_404(Blog, pk=id)

    if blog.author != request.user.username:
        return redirect('view_all')

    if request.method=="POST":
        form = BlogForm(request.POST, instance=blog)

        if form.is_valid():
            form.save()
            return redirect("view_all")
    
    else:
        form = BlogForm(instance=blog)
    
    return render(request, "update_blog.html", {"form": form})

@login_required
def delete_blog(request, id):
    blog = get_object_or_404(Blog, pk=id)

    if blog.author != request.user:
        return redirect('view_all')

    if request.method=="POST":
        blog.delete()

        return redirect("view_all")
    
    return render(request, "delete_blog.html")


def view_all(request):
    context = {}

    if request.user.is_authenticated:
        context['status'] = True
    else:
        context['status']= False

    blogs = Blog.objects.all()
    context['blogs'] = blogs

    return render(request, "view_all.html", context=context)


def view_blog(request, id):
    blog = get_object_or_404(Blog, pk=id)

    context = {}

    if request.user.is_authenticated:
        context['status'] = True
    else:
        context['status']= False
    context['blog'] = blog

    return render(request, "view_blog.html", context=context)
