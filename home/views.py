from django.shortcuts import render
from product.models import Product, ProductCategory

# Create your views here.

def home_view(request):

    html_file_name = 'home/home.html'

    # returning all category queryset
    all_categories = ProductCategory.objects.all()
    # returning all product queryset
    all_products = Product.objects.all()



    context = {
        'categories': all_categories,
        'products': all_products,
    }

    return render(request, html_file_name, context)