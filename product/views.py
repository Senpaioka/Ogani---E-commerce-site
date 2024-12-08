from django.shortcuts import render
from product.models import Product, ProductCategory

# Create your views here.


# all product page
def product_store_page(request):

    html_file_name = 'product/store.html'

    all_categories = ProductCategory.objects.all()
    all_products = Product.objects.all()
    

    context = {
        'categories': all_categories,
        'products': all_products,
    }

    return render(request, html_file_name, context)





# product details page
def single_product_page(request):
    
    html_file_name = 'product/product.html'

    context = {}

    return render(request, html_file_name, context)

