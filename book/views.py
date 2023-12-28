from django.shortcuts import render, redirect, HttpResponse, get_object_or_404

from django.views.generic import ListView
from django.views import View
from django.db.models import Q

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import UserForm, LoginForm, CheckoutForm
from .models import Books, Cart, Checkout


# Create your views here.

class UserRegister(View):
    def get(self, request):
        form = UserForm()
        return render(request, "form.html", {'form': form, 'request': request})
    
    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        
        else:
            return render(request, "form.html", {'form': form, 'request': request})

##############################################################################################

class UserLogin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "form.html", {'form': form, 'request': request})
    
    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("home")

        
        return render(request, "form.html", {'form': form, 'request': request})

##############################################################################################

class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect("home")

##############################################################################################

class BookDisplay(ListView):
    model = Books
    template_name = "home.html"
    context_object_name = "books"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        context['request'] = self.request
        return context

##############################################################################################

class CartDisplay(LoginRequiredMixin, View):
    model = Cart
    login_url = "/login/"

    def get(self, request):
        try:
            cart = self.model.objects.get(user=request.user)
            total = 0
            for x in cart.book.all():
                total += x.price

            return render(request, "cart.html", {'cart':cart, 'total': total, 'request': request})
        except:
            return HttpResponse("Cart is empty")
    
    def post(self, request):
        title = request.POST.get("title")
        author = request.POST.get("author")
        book = Books.objects.get(title=title, author=author)

        try:
            cart = self.model.objects.get(user=request.user)
        except:
            cart = self.model(user=request.user)
            cart.save()
        
        cart.book.add(book)
        cart.save()

        cart = self.model.objects.get(user=request.user)
        total = 0
        for x in cart.book.all():
            total += x.price

        return render(request, "cart.html", {'cart':cart, 'total': total, 'request': request})

##############################################################################################

class CheckoutView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/login/'

    def get(self, request):
        try:
            Cart.objects.get(user=request.user)
            form = CheckoutForm()
            return render(request, "form.html", {'form':form,'request': request})
        except:
            return HttpResponse("Cart is empty")
    
    def post(self, request):
        form = CheckoutForm(request.POST)

        if form.is_valid():
            cart = Cart.objects.get(user=request.user)
            
            checkout = form.save(commit=False)

            checkout.user = cart.user

            checkout.save()

            checkout.book.set(cart.book.all())

            cart.delete()
            
            return HttpResponse("Your order will be shipped within a minute")
        
        return render(request, "form.html", {'form':form, 'request':request})


    def test_func(self):
        cart = get_object_or_404(Cart, user=self.request.user)
        return self.request.user == cart.user

##############################################################################################

class OrderHistoryView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = "order_history.html"
    context_object_name = "checkout"
    model = Checkout

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['request'] = self.request

        checkout = self.model.objects.filter(user=self.request.user)

        total = 0

        for usr in checkout:
            for bk in usr.book.all():
                total += bk.price

        context['total'] = total

        return context
        
##############################################################################################

class SearchView(View):
    model = Books

    def post(self, request):
        print(request.POST)
        itm = request.POST.get('search')

        books = self.model.objects.filter(
            Q(title__icontains=itm) | Q(author__icontains=itm) | Q(desc__icontains=itm)
        )
        
        context = {
            'books': books,
            'request': request
        }

        return render(request, "home.html", context)




            