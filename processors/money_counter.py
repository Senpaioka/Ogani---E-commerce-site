from cart.models import CartProduct


def cart_total(request):

    try:
        current_user = request.user 
        if current_user.is_authenticated:
            cart = CartProduct.objects.filter(user=current_user)
            total = 0

            for item in cart:
                total += item.sub_total()

            tax = total * 0.1
            total += tax
        else:
            total = 0
    
    except CartProduct.DoesNotExist:
        total = 0

    return {'cart_total': total}

