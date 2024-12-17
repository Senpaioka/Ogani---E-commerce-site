from cart.models import CartID, CartProduct
from codelib.user_session import _user_session_key


def product_in_cart_count(request):

    product_count = 0
    current_user = request.user
    
    try:
        
        if current_user.is_authenticated:
            all_cart_products = CartProduct.objects.all().filter(user=current_user)
            product_count = all_cart_products.count()


    except CartProduct.DoesNotExist:
        product_count = 0
        

    return dict(counter = product_count)