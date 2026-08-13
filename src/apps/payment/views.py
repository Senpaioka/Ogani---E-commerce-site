from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from apps.cart.models import CartProduct
from apps.accounts.models import UserAccount
from apps.payment.models import PurchaseHistory
from apps.product.models import Product
import datetime
from django.conf import settings
from common.context_processors.money_counter import cart_total
from django.contrib.auth.decorators import login_required
from apps.payment.paypal_service import create_paypal_order, capture_paypal_order

# Create your views here.

@login_required
def checkout_page(request):
    html_template_name = 'payment/checkout.html'
    current_user = request.user
    get_cart_products = CartProduct.objects.filter(user=current_user).select_related('product')
    ordering_time = datetime.datetime.now()

    if request.method == "POST":
        get_bill = cart_total(request)
        bill = float(get_bill['cart_total'])
        
        scheme = 'https' if request.is_secure() else 'http'
        host = request.get_host()
        return_url = f"{scheme}://{host}{reverse('payment:payment_successful')}"
        cancel_url = f"{scheme}://{host}{reverse('payment:payment_failed')}"

        try:
            paypal_order = create_paypal_order(bill, return_url, cancel_url)
            if paypal_order.get("approval_url"):
                return redirect(paypal_order["approval_url"])
        except Exception as e:
            return render(request, html_template_name, {
                'buyer': current_user,
                'products': get_cart_products,
                'time': ordering_time,
                'error': str(e)
            })

    context = {
        'buyer': current_user,
        'products': get_cart_products,
        'time': ordering_time,
    }

    return render(request, html_template_name, context)


@login_required
def payment_success_view(request):
    html_template_name = 'payment/success.html'
    current_user = request.user
    token = request.GET.get('token') # PayPal Order ID returned on success redirect

    if token:
        try:
            capture_result = capture_paypal_order(token)
            status = capture_result.get('status')
            if status == 'COMPLETED':
                get_cart_products = CartProduct.objects.filter(user=current_user).select_related('product')
                purchases = [
                    PurchaseHistory(
                        user=current_user,
                        product=item.product,
                        is_purchased=True
                    )
                    for item in get_cart_products
                ]
                if purchases:
                    PurchaseHistory.objects.bulk_create(purchases)
                get_cart_products.delete()

                return render(request, html_template_name, {'status': 'COMPLETED'})
        except Exception as e:
            return redirect('payment:payment_failed')

    return render(request, html_template_name, {})


def payment_failed_view(request):
    html_template_name = 'payment/failed.html'
    context = {}
    return render(request, html_template_name, context)

