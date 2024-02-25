from django.shortcuts import render
from catalog.models import Product


def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'catalog/home.html', context)


def contact(request):
    return render(request, 'catalog/contact.html')


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    context = {'product': product}
    return render(request, 'catalog/product_detail.html', context)


def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'index.html', context)
