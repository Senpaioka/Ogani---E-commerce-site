from django.shortcuts import render, redirect
from codelib.user_session import _user_session_key
from cart.models import CartID, CartProduct
from product.models import Product
from accounts.models import UserAccount

# Create your views here.


def main_cart_page(request):

    html_template_name = 'cart/cart.html'

    current_user = request.user

    if current_user.is_authenticated:

        user_cart_products = CartProduct.objects.filter(user=current_user)

    context = {
        'all_products': user_cart_products,
    }

    return render(request, html_template_name, context)







def add_product_into_cart(request, product_id):

    current_user = request.user

    if current_user.is_authenticated:

        # getting selected product details
        get_product = Product.objects.get(pk=product_id)

        # getting user session if exists
        user_session = _user_session_key(request)

        # saving user session in CartID model
        try:
            cart_id = CartID.objects.get(cart_id=user_session)

        except CartID.DoesNotExist:
            cart_id = CartID.objects.create(cart_id=_user_session_key(request))
        
        cart_id.save()


        all_cart_products = CartProduct.objects.filter(user=current_user)

        product_in_cart = []
        if all_cart_products.exists():
            for value in all_cart_products.values():
                product_in_cart.append(value['product_id'])


        if get_product.id in product_in_cart:

            cart_product = CartProduct.objects.get(product=get_product)
            cart_product.quantity += 1
            cart_product.save()
            
        
        else:
            # saving user session and product info in CartProduct model
            cart_product = CartProduct.objects.create(
                user = current_user,
                user_session = cart_id,
                product = get_product,
                quantity = 1,
                price = get_product.product_price,
            )
            cart_product.save()
        
    return redirect('cart:cart_page')











def increase_product_quantity(request, product_id):

    current_user = request.user

    if current_user.is_authenticated:

        # getting selected product details
        get_product = Product.objects.get(pk=product_id)
        cart_product = CartProduct.objects.get(product__product_name = get_product)
        
        cart_product.quantity += 1
        cart_product.save()


    return redirect('cart:cart_page')
    









def decrease_product_quantity(request, product_id):

    current_user = request.user

    if current_user.is_authenticated:

        # getting selected product details
        get_product = Product.objects.get(pk=product_id)
        cart_product = CartProduct.objects.get(product__product_name = get_product)
        
        if cart_product.quantity > 1:
            cart_product.quantity -= 1
            cart_product.save()
        
        else:
            cart_product.delete()


    return redirect('cart:cart_page')






def delete_cart_product(request, product_id):

    current_user = request.user

    if current_user.is_authenticated:

        # getting selected product to delete
        get_product = Product.objects.get(pk=product_id)
        cart_product = CartProduct.objects.get(product__product_name = get_product)
        
        cart_product.delete()

    return redirect('cart:cart_page')
