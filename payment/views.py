from django.shortcuts import render
from cart.models import CartProduct
from accounts.models import UserAccount
import datetime

# Create your views here.


def checkout_page(request):

    html_template_name = 'payment/checkout.html'

    current_user = request.user
    if current_user.is_authenticated:
        # getting cart product info
        get_cart_products = CartProduct.objects.filter(user=current_user)
        # getting user info
        user_detail_info = UserAccount.objects.get(username=current_user)

        # getting order time
        ordering_time = datetime.datetime.now()

    context = {
        'buyer': user_detail_info,
        'products': get_cart_products,
        'time': ordering_time,
    }

    return render(request, html_template_name, context)

