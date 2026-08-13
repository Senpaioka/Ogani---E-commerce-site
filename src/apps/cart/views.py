from django.shortcuts import render, redirect, get_object_or_404
from common.utils.user_session import _user_session_key
from apps.cart.models import CartID, CartProduct, UserWishList
from apps.product.models import Product
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def main_cart_page(request):

    html_template_name = 'cart/cart.html'

    current_user = request.user
    user_cart_products = CartProduct.objects.filter(user=current_user).select_related('product', 'product__product_category')

    # calculate all product price
    total_price = 0
    tax_percent = 0.1 # 10%

    for data in user_cart_products:
        total_price += data.product.product_price * data.quantity

    # calculate tax
    tax = round(total_price * tax_percent, 2)
    final_price = total_price + tax

    context = {
        'all_products': user_cart_products,
        'total_price': total_price,
        'final_price': final_price,
        'tax': tax,
    }

    return render(request, html_template_name, context)


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


