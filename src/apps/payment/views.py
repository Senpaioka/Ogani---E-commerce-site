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

from apps.cart.models import CartProduct, Coupon

@login_required
def checkout_page(request):
    html_template_name = 'payment/checkout.html'
    current_user = request.user
    get_cart_products = list(CartProduct.objects.filter(user=current_user).select_related('product'))
    ordering_time = datetime.datetime.now()

    coupon_code = request.session.get('coupon_code')
    applied_coupon = None
    if coupon_code:
        applied_coupon = Coupon.objects.filter(code__iexact=coupon_code, is_active=True).first()

    raw_total = sum(item.product.product_price * item.quantity for item in get_cart_products)
    discount_amount = 0

    for item in get_cart_products:
        item_raw = item.product.product_price * item.quantity
        if applied_coupon and applied_coupon.product_id and applied_coupon.product_id == item.product_id:
            item_disc = round(item_raw * (applied_coupon.discount_percentage / 100.0), 2)
            item.discount_amount = item_disc
            item.discounted_subtotal = round(item_raw - item_disc, 2)
            item.has_coupon = True
            discount_amount += item_disc
        else:
            item.discount_amount = 0
            item.discounted_subtotal = round(item_raw, 2)
            item.has_coupon = False

    subtotal_after_discount = max(0.0, raw_total - discount_amount)
    tax = round(subtotal_after_discount * 0.1, 2)
    final_price = round(subtotal_after_discount + tax, 2)

    if request.method == "POST":
        bill = float(final_price)
        
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
                'raw_total': round(raw_total, 2),
                'discount_amount': round(discount_amount, 2),
                'subtotal_after_discount': round(subtotal_after_discount, 2),
                'tax': tax,
                'final_price': final_price,
                'applied_coupon': applied_coupon,
                'error': str(e)
            })

    context = {
        'buyer': current_user,
        'products': get_cart_products,
        'time': ordering_time,
        'raw_total': round(raw_total, 2),
        'discount_amount': round(discount_amount, 2),
        'subtotal_after_discount': round(subtotal_after_discount, 2),
        'tax': tax,
        'final_price': final_price,
        'applied_coupon': applied_coupon,
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

