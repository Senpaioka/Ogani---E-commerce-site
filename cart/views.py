from django.shortcuts import render, redirect
from codelib.user_session import _user_session_key
from cart.models import CartID, CartProduct, UserWishList
from product.models import Product

# Create your views here.


def main_cart_page(request):

    html_template_name = 'cart/cart.html'

    current_user = request.user

    if current_user.is_authenticated:

        user_cart_products = CartProduct.objects.filter(user=current_user)

        # calculate all product price
        total_price = 0
        tax_percent = 0.1 # 10%

        for data in user_cart_products:
            total_price += data.product.product_price * data.quantity

        # calculate tax
        tax = round(total_price * tax_percent, 2) # example: 5.00
        final_price = total_price + tax


    context = {
        'all_products': user_cart_products,
        'total_price': total_price,
        'final_price': final_price,
        'tax': tax,
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

        # add new product if already not exists in cart
        all_cart_products = CartProduct.objects.filter(user=current_user)

        product_in_cart = []
        if all_cart_products.exists():
            for value in all_cart_products.values():
                product_in_cart.append(value['product_id'])

        # if product exists in the cart
        if get_product.id in product_in_cart:

            cart_product = CartProduct.objects.get(product=get_product)
            cart_product.quantity += 1
            cart_product.save()
            
        
        else:
            # if not exists crate product info in CartProduct model
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









# wishlist functionality

def wishlist_main_page(request):

    html_template_name = 'cart/wishlist.html'

    current_user = request.user

    if current_user.is_authenticated:

        get_user_wishlist = UserWishList.objects.all().filter(user=current_user)




    context = {
        'wishlist': get_user_wishlist,
    }

    return render(request, html_template_name, context)








def wishlist_add_product(request, product_id):

    current_user = request.user

    if current_user.is_authenticated:
        
        get_product = Product.objects.get(pk=product_id)
        get_wishlist = UserWishList.objects.filter(product__pk=get_product.id)
        


        if get_wishlist.exists():
            set_wishlist = UserWishList.objects.get(product=get_product)
            if set_wishlist.is_wishlist == False:
                set_wishlist.is_wishlist = True
                set_wishlist.save()
            else:
                set_wishlist.is_wishlist = False
                set_wishlist.save() 
       
        else:
            user_wishlist = UserWishList.objects.create(
                user = current_user,
                product = get_product,
                is_wishlist = True,
            )

            user_wishlist.save()


    return redirect(request.META['HTTP_REFERER'])
    
