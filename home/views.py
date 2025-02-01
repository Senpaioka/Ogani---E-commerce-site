from django.shortcuts import render
from product.models import Product, ProductCategory
from home.search_form import ProductSearchForm
from django.db.models import Q
from django.core.paginator import Paginator
from blog.models import BlogModel, BlogCommentTracker
from review.models import ProductReview

# Create your views here.

def home_view(request):

    html_file_name = 'home/home.html'

    # returning all category queryset
    all_categories = ProductCategory.objects.all()
    # returning all product queryset
    all_products = Product.objects.all()

    # enabling search field
    user_search_key = ProductSearchForm()

    # getting 3 blog
    getting_blogs = BlogModel.objects.all().order_by('-created_at')[:3]
    blogs_with_comments = BlogCommentTracker.objects.all()[:3]

    # getting latest products
    latest_product_one = Product.objects.all().order_by('updated_at')[:3]
    latest_product_two = Product.objects.all().order_by('updated_at')[4:7]

    # getting top rated products
    top_products = ProductReview.objects.all().order_by('star')[:3]

    # getting reviewed products
    reviewed_product = ProductReview.objects.all().order_by('created_at')[:3]



    context = {
        'categories': all_categories,
        'products': all_products,
        'search_form': user_search_key,
        'blogs': getting_blogs,
        'new_product_one': latest_product_one,
        'new_product_two': latest_product_two,
        'top_product': top_products,
        'latest_reviewed': reviewed_product,
        'commented_blogs': blogs_with_comments, 
    }

    return render(request, html_file_name, context)




def product_search_view(request):

    html_template_name = 'home/search.html'

    # getting user's search words

    get_user_keyword = ProductSearchForm(request.GET or None)
    result = []

    if get_user_keyword.is_valid():
        user_input = get_user_keyword.cleaned_data.get('search_key')
        result = Product.objects.filter(
            Q(product_name__icontains=user_input) | Q(product_info__icontains=user_input) | Q(product_description__icontains=user_input)
        )

        paginator = Paginator(result, 6) 
        page_number = request.GET.get('page')
        search_results = paginator.get_page(page_number)
    
    else:
        get_user_keyword = ProductSearchForm()

    # getting latest products
    latest_product_one = Product.objects.all().order_by('updated_at')[:3]
    latest_product_two = Product.objects.all().order_by('updated_at')[4:7]

    context = {
    'paged_result': search_results,
    'keyword': user_input,
    'total_result': result,
    'new_product_one': latest_product_one,
    'new_product_two': latest_product_two,
    }

    return render(request, html_template_name, context)