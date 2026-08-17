from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.product.models import Product
from apps.review.models import ProductReview
from apps.payment.models import PurchaseHistory

# Create your views here.


@login_required
def review_page_view(request, product_id):
    html_template_name = 'review/review.html'
    get_product = get_object_or_404(Product, id=product_id)
    current_user = request.user

    is_purchased = PurchaseHistory.objects.filter(user=current_user, product=get_product, is_purchased=True).exists()
    if not is_purchased:
        messages.error(request, "Only verified buyers who have purchased this product can leave a review.")
        return redirect('product:single_product', product_id=product_id)

    existing_review = ProductReview.objects.filter(user=current_user, product=get_product).first()

    context = {
        'id': product_id,
        'product': get_product,
        'existing_review': existing_review,
    }

    return render(request, html_template_name, context)


@login_required
def review_publish_view(request, product_id):
    get_product = get_object_or_404(Product, id=product_id)
    current_user = request.user

    is_purchased = PurchaseHistory.objects.filter(user=current_user, product=get_product, is_purchased=True).exists()
    if not is_purchased:
        messages.error(request, "Only verified buyers who have purchased this product can leave a review.")
        return redirect('product:single_product', product_id=product_id)

    if request.method == "POST":
        rating_value = int(request.POST.get("rating", 0))
        review_value = request.POST.get("text_value", "").strip()

        if rating_value > 0 and review_value:
            ProductReview.objects.update_or_create(
                user=current_user,
                product=get_product,
                defaults={
                    'star': rating_value,
                    'review': review_value,
                }
            )
            messages.success(request, "Thank you! Your product review has been submitted.")
        else:
            messages.error(request, "Please select a rating and provide review feedback.")
            return redirect('review:review_page', product_id=product_id)

    return redirect('product:single_product', product_id=product_id)



    