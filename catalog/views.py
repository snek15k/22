from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Product


def home_view(request):
    products = Product.objects.all()
    return render(request, 'catalog/home.html', {'products': products})

def contacts_view(request):
    success = False
    if request.method == 'POST':
        message = request.POST.get('message')

        success = True
    return render(request, 'catalog/contacts.html', {'success': success})


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})
