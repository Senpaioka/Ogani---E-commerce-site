from django.shortcuts import render
from product.models import Product, ProductCategory, ProductGallery
from django.core.paginator import Paginator
from cart.models import UserWishList
from payment.models import PurchaseHistory
from review.models import ProductReview
# Create your views here.


# all product page
def product_store_page(request):

    html_file_name = 'product/store.html'

    all_categories = ProductCategory.objects.all()
    all_products = Product.objects.all()
    # paginator
    paginator = Paginator(all_products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # getting latest products
    latest_product_one = Product.objects.all().order_by('updated_at')[:3]
    latest_product_two = Product.objects.all().order_by('updated_at')[4:7]
    

    context = {
        'categories': all_categories,
        'products': all_products,
        'pages': page_obj,
        'new_product_one': latest_product_one,
        'new_product_two': latest_product_two,
    }

    return render(request, html_file_name, context)





# product details page
def single_product_page(request, product_id):
    
    html_file_name = 'product/product.html'

    # getting user wishlist info
    current_user = request.user

    if current_user.is_authenticated:
        user_wishlist = UserWishList.objects.filter(product__pk=product_id)
        if user_wishlist.exists():
            wishlist_or_not = user_wishlist[0].is_wishlist
        else:
            wishlist_or_not = False
            
    else:
         wishlist_or_not = False



    # getting selected product
    selected_product = Product.objects.get(pk=product_id)
    thumb_img = ProductGallery.objects.filter(product__pk=product_id)
    
    # returning only first 4 item for display
    related_category_product = Product.objects.filter(product_category=selected_product.product_category)[:4]


    # check if user purchase a product or not

    purchase_checker = PurchaseHistory.objects.filter(product__product_name=selected_product)
    is_user_purchased = False
    if purchase_checker:
        for value in purchase_checker:
            if value.user == current_user and value.is_purchased == True:
                is_user_purchased = True
            
    # get all product specific reviews
    get_reviews = ProductReview.objects.filter(product__pk=product_id)
    review_count = 0
    if get_reviews:
        review_count = get_reviews.count()


    # star counting functionality
    star_total = 0
    star_avg = 0
    if get_reviews:
        for user_stars in get_reviews:
            star_total += user_stars.star 
            star_avg = round(star_total / review_count)

    


    context = {
        'product': selected_product,
        'small_image': thumb_img,
        'related_products': related_category_product,
        'check_wishlist': wishlist_or_not,
        'purchased_user': is_user_purchased,
        'all_review': get_reviews,
        'review_count': review_count,
        'avg_star': star_avg,
    }

    return render(request, html_file_name, context)




def product_by_category_page(request, category_name):

    html_file_name = 'product/category.html'

    product_by_category = Product.objects.filter(product_category__product_category=category_name)
    selected_category = category_name

    paginator = Paginator(product_by_category, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # getting latest products
    latest_product_one = Product.objects.all().order_by('updated_at')[:3]
    latest_product_two = Product.objects.all().order_by('updated_at')[4:7]

    context = {
        'category_product': product_by_category,
        'category': selected_category,
        'pages': page_obj,
        'new_product_one': latest_product_one,
        'new_product_two': latest_product_two,
    }

    return render(request, html_file_name, context)