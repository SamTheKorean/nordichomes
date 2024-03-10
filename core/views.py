from django.contrib.auth import login 
from django.shortcuts import render, redirect
from product.models import Product, Category
from django.db.models import Q

from .forms import SignUpForm
def frontpage(request):
    products = Product.objects.all()[0:8]

    return render(request, 'core/frontpage.html',{'products':products})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('/')
    else:
        form = SignUpForm()

    return render(request, 'core/signup.html', {'form':form})

def login_old(request):
    return render(request, 'core/login.html')

def shop(request):
    products = Product.objects.all()
    categories = Category.objects.all()[0:5]

    active_category = request.GET.get('category', '')

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    if q:
        products = Product.objects.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )

    if active_category:
        products = products.filter(category__slug=active_category)

    context = {
        'categories': categories,
        'products':products,
        'active_category': active_category
    }

    return render(request, 'core/shop.html',context)