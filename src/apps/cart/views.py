from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from common.utils.user_session import _user_session_key
from apps.cart.models import CartID, CartProduct, UserWishList, Coupon
from apps.product.models import Product
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def main_cart_page(request):

    html_template_name = 'cart/cart.html'

    current_user = request.user
    user_cart_products = list(CartProduct.objects.filter(user=current_user).select_related('product', 'product__product_category'))

    # calculate all product price
    total_price = 0
    tax_percent = 0.1 # 10%

    coupon_code = request.session.get('coupon_code')
    applied_coupon = None
    if coupon_code:
        applied_coupon = Coupon.objects.filter(code__iexact=coupon_code, is_active=True).first()

    total_discount_amount = 0

    for data in user_cart_products:
        item_raw_subtotal = data.product.product_price * data.quantity
        data.raw_subtotal = round(item_raw_subtotal, 2)
        total_price += item_raw_subtotal

        if applied_coupon and applied_coupon.product_id and applied_coupon.product_id == data.product_id:
            item_discount = round(item_raw_subtotal * (applied_coupon.discount_percentage / 100.0), 2)
            data.discount_amount = item_discount
            data.discounted_subtotal = round(item_raw_subtotal - item_discount, 2)
            data.has_coupon = True
            total_discount_amount += item_discount
        else:
            data.discount_amount = 0
            data.discounted_subtotal = round(item_raw_subtotal, 2)
            data.has_coupon = False

    if applied_coupon and not any(data.has_coupon for data in user_cart_products):
        applied_coupon = None
        total_discount_amount = 0
        request.session.pop('coupon_code', None)

    subtotal_after_discount = max(0.0, total_price - total_discount_amount)
    tax = round(subtotal_after_discount * tax_percent, 2)
    final_price = round(subtotal_after_discount + tax, 2)

    context = {
        'all_products': user_cart_products,
        'total_price': round(total_price, 2),
        'discount_amount': round(total_discount_amount, 2),
        'subtotal_after_discount': round(subtotal_after_discount, 2),
        'applied_coupon': applied_coupon,
        'final_price': final_price,
        'tax': tax,
    }

    return render(request, html_template_name, context)



@login_required
def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('coupon_code', '').strip()
        if not code:
            messages.error(request, "Please enter a coupon code.")
            return redirect('cart:cart_page')

        coupon = Coupon.objects.filter(code__iexact=code, is_active=True).first()
        if not coupon:
            messages.error(request, f"Coupon code '{code}' is invalid or inactive.")
            return redirect('cart:cart_page')

        if not coupon.product:
            messages.error(request, f"Coupon '{coupon.code}' is not valid for any specific product.")
            return redirect('cart:cart_page')

        cart_has_product = CartProduct.objects.filter(user=request.user, product=coupon.product).exists()
        if not cart_has_product:
            messages.warning(request, f"Coupon '{coupon.code}' applies to '{coupon.product.product_name}', which is not in your cart.")
            return redirect('cart:cart_page')

        request.session['coupon_code'] = coupon.code
        messages.success(request, f"Coupon '{coupon.code}' applied! Saved {coupon.discount_percentage}% on {coupon.product.product_name}.")

    return redirect('cart:cart_page')


@login_required
def remove_coupon(request):
    if 'coupon_code' in request.session:
        del request.session['coupon_code']
        messages.info(request, "Coupon removed.")
    return redirect('cart:cart_page')



@login_required
def add_product_into_cart(request, product_id):

    current_user = request.user
    get_product = get_object_or_404(Product, pk=product_id)

    user_session = _user_session_key(request)
    cart_id, _ = CartID.objects.get_or_create(cart_id=user_session)

    # Atomic lookup scoped to the logged-in user
    cart_product, created = CartProduct.objects.get_or_create(
        user=current_user,
        product=get_product,
        defaults={
            'user_session': cart_id,
            'price': get_product.product_price,
            'quantity': 1,
        }
    )
    if not created:
        cart_product.quantity += 1
        cart_product.save()

    return redirect('cart:cart_page')


@login_required
def increase_product_quantity(request, product_id):

    cart_product = get_object_or_404(CartProduct, user=request.user, product_id=product_id)
    cart_product.quantity += 1
    cart_product.save()

    return redirect('cart:cart_page')


@login_required
def decrease_product_quantity(request, product_id):

    cart_product = get_object_or_404(CartProduct, user=request.user, product_id=product_id)
    
    if cart_product.quantity > 1:
        cart_product.quantity -= 1
        cart_product.save()
    else:
        cart_product.delete()

    return redirect('cart:cart_page')


@login_required
def delete_cart_product(request, product_id):

    CartProduct.objects.filter(user=request.user, product_id=product_id).delete()

    return redirect('cart:cart_page')


# wishlist functionality
@login_required
def wishlist_main_page(request):

    html_template_name = 'cart/wishlist.html'

    get_user_wishlist = UserWishList.objects.filter(
        user=request.user, 
        is_wishlist=True
    ).select_related('product', 'product__product_category')

    context = {
        'wishlist': get_user_wishlist,
    }

    return render(request, html_template_name, context)


@login_required
def wishlist_add_product(request, product_id):

    current_user = request.user
    get_product = get_object_or_404(Product, pk=product_id)

    wishlist_item, created = UserWishList.objects.get_or_create(
        user=current_user,
        product=get_product,
        defaults={'is_wishlist': True}
    )
    if not created:
        wishlist_item.is_wishlist = not wishlist_item.is_wishlist
        wishlist_item.save()

    referer = request.META.get('HTTP_REFERER')
    return redirect(referer if referer else 'home:home_page')


@login_required
def remove_wishlist_product(request, product_id):

    UserWishList.objects.filter(user=request.user, product_id=product_id).delete()

    return redirect('cart:wishlist_page')


