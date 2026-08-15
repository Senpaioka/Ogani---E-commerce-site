from django.shortcuts import render, get_object_or_404
from apps.product.models import Product, ProductCategory, ProductGallery
from django.core.paginator import Paginator
from apps.cart.models import UserWishList
from apps.payment.models import PurchaseHistory
from apps.review.models import ProductReview
# Create your views here.


# all product page
def product_store_page(request):

    html_file_name = 'product/store.html'

    sort_option = request.GET.get('sort', 'default')

    all_categories = ProductCategory.objects.all()
    all_products = Product.objects.select_related('product_category').all()

    if sort_option == 'price_low':
        all_products = all_products.order_by('product_price')
    elif sort_option == 'price_high':
        all_products = all_products.order_by('-product_price')
    elif sort_option == 'newest':
        all_products = all_products.order_by('-created_at')

    # paginator
    paginator = Paginator(all_products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # getting latest products
    latest_product_one = Product.objects.select_related('product_category').order_by('-updated_at')[:3]
    latest_product_two = Product.objects.select_related('product_category').order_by('-updated_at')[3:6]
    

    # getting discount/featured products
    discount_products = Product.objects.select_related('product_category').filter(is_available=True)[:6]

    context = {
        'categories': all_categories,
        'products': all_products,
        'pages': page_obj,
        'new_product_one': latest_product_one,
        'new_product_two': latest_product_two,
        'discount_products': discount_products,
        'current_sort': sort_option,
    }

    return render(request, html_file_name, context)





# product details page
def single_product_page(request, product_id):
    
    html_file_name = 'product/product.html'

    current_user = request.user

    # checking wishlist status with efficient DB query
    if current_user.is_authenticated:
        wishlist_or_not = UserWishList.objects.filter(user=current_user, product_id=product_id, is_wishlist=True).exists()
        is_user_purchased = PurchaseHistory.objects.filter(user=current_user, product_id=product_id, is_purchased=True).exists()
    else:
        wishlist_or_not = False
        is_user_purchased = False

    # getting selected product safely with pre-joined category
    selected_product = get_object_or_404(Product.objects.select_related('product_category'), pk=product_id)
    thumb_img = ProductGallery.objects.filter(product_id=product_id)
    
    # returning related products
    related_category_product = Product.objects.filter(product_category=selected_product.product_category).select_related('product_category').exclude(pk=product_id)[:4]

    # get product reviews with user pre-fetched to avoid N+1 queries in template
    get_reviews = ProductReview.objects.filter(product_id=product_id).select_related('user')
    review_count = get_reviews.count()

    # star calculation
    star_total = sum(user_stars.star for user_stars in get_reviews) if review_count > 0 else 0
    star_avg = round(star_total / review_count) if review_count > 0 else 0

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

    product_by_category = Product.objects.filter(product_category__product_category=category_name).select_related('product_category')
    selected_category = category_name

    paginator = Paginator(product_by_category, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # getting latest products
    latest_product_one = Product.objects.select_related('product_category').order_by('-updated_at')[:3]
    latest_product_two = Product.objects.select_related('product_category').order_by('-updated_at')[3:6]

    context = {
        'category_product': product_by_category,
        'category': selected_category,
        'pages': page_obj,
        'new_product_one': latest_product_one,
        'new_product_two': latest_product_two,
    }

    return render(request, html_file_name, context)