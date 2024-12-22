from cart.models import UserWishList

def wishlist_counter(request):

    current_user = request.user
    count_wishlist = 0

    try:
        if current_user.is_authenticated:
            get_wishlist_products = UserWishList.objects.all().filter(user=current_user, is_wishlist=True)
            count_wishlist = get_wishlist_products.count()
    
        else:
            count_wishlist = 0
            
    except UserWishList.DoesNotExist:
        count_wishlist = 0

    return {'count_wishlist': count_wishlist}

