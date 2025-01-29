from django.shortcuts import render, HttpResponse
from django.urls import reverse
from cart.models import CartProduct
from accounts.models import UserAccount
from payment.models import PurchaseHistory
from product.models import Product
import datetime
from django.conf import settings
import uuid
# paypal
from paypal.standard.forms import PayPalPaymentsForm
from processors.money_counter import cart_total


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
        # getting host
        host = request.get_host()
    
        get_bill = cart_total(request)
        bill = int(get_bill['cart_total'])

        # paypal getaway
        paypal_dict = {
        "business": settings.RECEIVER_EMAIL,
        "amount": bill,
        "item_name": "Products From Ogani",
        "invoice": str(uuid.uuid4()),
        "currency_code": 'USD',
        "notify_url": 'http://{}{}'.format(host, reverse('paypal-ipn')),
        "return": 'http://{}{}'.format(host, reverse('payment:payment_successful')),
        "cancel_return": request.build_absolute_uri(reverse('payment:payment_failed')),
        }
        
        paypal_form = PayPalPaymentsForm(initial=paypal_dict)

    context = {
        'buyer': user_detail_info,
        'products': get_cart_products,
        'time': ordering_time,
        'paypal': paypal_form,
    }

    return render(request, html_template_name, context)



def payment_success_view(request):
    html_template_name = 'payment/success.html'

    current_user = request.user
    if current_user.is_authenticated:
        get_cart_products = CartProduct.objects.filter(user=current_user)
        
        for item in get_cart_products:
            get_product = Product.objects.get(product_name=item.product)
            # creating purchase history
            PurchaseHistory.objects.create(
                user = current_user,
                product = get_product,
                is_purchased = True
            ).save()

        # deleting cart product
        get_cart_products.delete()
    context = {}
    return render(request, html_template_name, context)



def payment_failed_view(request):
    html_template_name = 'payment/failed.html'
    context = {}
    return render(request, html_template_name, context)
