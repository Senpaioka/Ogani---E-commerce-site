from apps.cart.models import CartProduct, Coupon

# total price with tax
def cart_total(request):

    try:
        current_user = request.user 
        if current_user.is_authenticated:
            cart = CartProduct.objects.filter(user=current_user)
            total = 0

            for item in cart:
                total += item.sub_total()

            coupon_code = request.session.get('coupon_code')
            if coupon_code:
                coupon = Coupon.objects.filter(code__iexact=coupon_code, is_active=True).first()
                if coupon and coupon.product:
                    cart_item = cart.filter(product=coupon.product).first()
                    if cart_item:
                        discount = (cart_item.product.product_price * cart_item.quantity) * (coupon.discount_percentage / 100.0)
                        total = max(0.0, total - discount)

            tax = total * 0.1
            total = round(total + tax, 2)
        else:
            total = 0
    
    except CartProduct.DoesNotExist:
        total = 0

    return {'cart_total': total}



# total price without tax
def cart_total_without_tax(request):

    try:
        current_user = request.user 
        if current_user.is_authenticated:
            cart = CartProduct.objects.filter(user=current_user)
            total = 0

            for item in cart:
                total += item.sub_total()

            coupon_code = request.session.get('coupon_code')
            if coupon_code:
                coupon = Coupon.objects.filter(code__iexact=coupon_code, is_active=True).first()
                if coupon and coupon.product:
                    cart_item = cart.filter(product=coupon.product).first()
                    if cart_item:
                        discount = (cart_item.product.product_price * cart_item.quantity) * (coupon.discount_percentage / 100.0)
                        total = max(0.0, total - discount)

        else:
            total = 0
    
    except CartProduct.DoesNotExist:
        total = 0

    return {'total_without_tax': round(total, 2)}


