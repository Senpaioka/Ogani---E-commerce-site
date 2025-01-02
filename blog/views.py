from django.shortcuts import render, redirect
from blog.models import BlogModel, BlogCategory
from django.core.paginator import Paginator
from blog.blog_search import BlogSearchForm
from django.db.models import Q
from blog.blog_form import BlogPostForm

# Create your views here.

def blog_page(request):

    html_template_name = 'blog/blog.html'

    all_blogs = BlogModel.objects.all().order_by('-created_at')

    paginator = Paginator(all_blogs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    category_list = BlogCategory.objects.all()

    # form functionality
    blog_search_field = BlogSearchForm()

    # latest blogs
    latest_blogs = BlogModel.objects.all().order_by('-created_at')[:3]



    context = {
        'blogs': all_blogs,
        'pages': page_obj,
        'categories': category_list,
        'form': blog_search_field,
        'recent_blogs': latest_blogs,
    }

    return render(request, html_template_name, context)









def blog_details_page(request, blog_id):

    html_template_name = 'blog/blog_details.html'

    get_blog = BlogModel.objects.get(pk=blog_id)

    category = get_blog.blog_category
    get_relative_blogs = BlogModel.objects.filter(blog_category=category)
    remove_current_blog = get_relative_blogs.exclude(pk=blog_id)
    recommended_blogs = remove_current_blog[:3]

    # getting all category
    category_list = BlogCategory.objects.all()

    # form functionality
    blog_search_field = BlogSearchForm()

    # latest blogs
    latest_blogs = BlogModel.objects.all().order_by('-created_at')[:3]

    context = {
        'blog': get_blog,
        'read_more': recommended_blogs,
        'categories': category_list,
        'form': blog_search_field,
        'recent_blogs': latest_blogs,
    }

    return render(request, html_template_name, context)





def category_blog_page(request, category_id):

    html_template_name = 'blog/category_blog.html'

    get_blog_by_category = BlogModel.objects.filter(blog_category=category_id)

    #paginator
    paginator = Paginator(get_blog_by_category, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # getting all category
    category_list = BlogCategory.objects.all()

    # form functionality
    blog_search_field = BlogSearchForm()



    context = {
        'pages': page_obj,
        'categories': category_list,
        'form': blog_search_field,
    }

    return render(request, html_template_name, context)










def blog_search_functionality(request):

    html_template_name = 'blog/blog_search.html'

    # getting user's search words

    get_keyword = BlogSearchForm(request.GET or None)
    result = []

    if get_keyword.is_valid():
        user_input = get_keyword.cleaned_data.get('search_key')
        result = BlogModel.objects.filter(
            Q(title__icontains=user_input) | Q(blog_body__icontains=user_input)
        )

        paginator = Paginator(result, 6) 
        page_number = request.GET.get('page')
        search_results = paginator.get_page(page_number)
    
    else:
        get_keyword = BlogSearchForm()

    context = {
    'pages': search_results,
    'keyword': user_input,
    'total_result': result,
    }

    return render(request, html_template_name, context)







def blog_post_page(request):

    html_template_name = 'blog/blog_post.html'

    blog_post_form = BlogPostForm()

    context = {
        'form': blog_post_form,
    }

    return render(request, html_template_name, context)







def publish_blog_view(request):

    current_user = request.user

    if current_user.is_authenticated:
        
        if request.method == 'POST':
            
            get_blog = BlogPostForm(request.POST, request.FILES)
            
            if get_blog.is_valid():
                get_blog.cleaned_data.get('title')
                get_blog.cleaned_data.get('blog_body')

                saving_blog = get_blog.save(commit=False)
                saving_blog.author = current_user
                saving_blog.save()


    return redirect('blog:blog_page')



