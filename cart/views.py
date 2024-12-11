from django.shortcuts import render

# Create your views here.


def main_cart_page(request):

    html_template_name = 'cart/cart.html'

    context = {}

    return render(request, html_template_name, context)
