from django.shortcuts import render, get_object_or_404, redirect
from product.models import Product
from review.models import ProductReview

# Create your views here.

def review_page_view(request, product_id):

    html_template_name = 'review/review.html'    

    context = {
        'id': product_id,
    }

    return render(request, html_template_name, context)






def review_publish_view(request, product_id):
    
    get_product = get_object_or_404(Product, id=product_id)
    current_user = request.user

    if current_user.is_authenticated:

        if request.method == "POST":
            rating_value = int(request.POST.get("rating", 0))
            review_value = request.POST.get("text_value")

            ProductReview.objects.create(
                user = current_user,
                product = get_product,
                star = rating_value,
                review = review_value,
            ).save()

    return redirect('home:home_page')


    