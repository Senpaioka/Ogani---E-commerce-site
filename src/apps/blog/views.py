from django.shortcuts import render, redirect, get_object_or_404
from apps.blog.models import BlogModel, BlogCategory, BlogCommentModel, BlogCommentTracker
from django.core.paginator import Paginator
from apps.blog.blog_search import BlogSearchForm
from django.db.models import Q
from apps.blog.blog_form import BlogPostForm, UpdateBlogForm
import datetime
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import member_required
from django.utils.html import escape
from django.http import HttpResponseRedirect, HttpResponse
# Create your views here.


def blog_page(request):

    html_template_name = 'blog/blog.html'

    # showing blogs with comments pre-joined
    blogs_with_comments = BlogCommentTracker.objects.select_related('blog', 'blog__author', 'blog__blog_category').all()

    # paginator with pre-joined author and category
    all_blogs = BlogModel.objects.select_related('author', 'blog_category').order_by('-created_at')
    
    paginator = Paginator(all_blogs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    category_list = BlogCategory.objects.all()

    # form functionality
    blog_search_field = BlogSearchForm()

    # latest blogs
    latest_blogs = BlogModel.objects.select_related('author', 'blog_category').order_by('-created_at')[:3]

    context = {
        'pages': page_obj,
        'categories': category_list,
        'form': blog_search_field,
        'recent_blogs': latest_blogs,
        'commented_blogs': blogs_with_comments, 
    }

    return render(request, html_template_name, context)


def blog_details_page(request, blog_id):

    html_template_name = 'blog/blog_details.html'

    get_blog = get_object_or_404(BlogModel.objects.select_related('author', 'blog_category'), pk=blog_id)

    category = get_blog.blog_category
    get_relative_blogs = BlogModel.objects.filter(blog_category=category).select_related('author', 'blog_category')
    recommended_blogs = get_relative_blogs.exclude(pk=blog_id)[:3]

    # getting all category
    category_list = BlogCategory.objects.all()

    # form functionality
    blog_search_field = BlogSearchForm()

    # latest blogs
    latest_blogs = BlogModel.objects.select_related('author', 'blog_category').order_by('-created_at')[:3]

    # getting all blog comments with user attached
    get_comment = BlogCommentModel.objects.filter(blog_id=blog_id).select_related('user')

    context = {
        'blog': get_blog,
        'read_more': recommended_blogs,
        'categories': category_list,
        'form': blog_search_field,
        'recent_blogs': latest_blogs,
        'blog_id': blog_id,
        'comments': get_comment,
    }

    return render(request, html_template_name, context)


def category_blog_page(request, category_id):

    html_template_name = 'blog/category_blog.html'

    get_blog_by_category = BlogModel.objects.filter(blog_category=category_id).select_related('author', 'blog_category')

    #paginator
    paginator = Paginator(get_blog_by_category, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # getting all category
    category_list = BlogCategory.objects.all()

    # form functionality
    blog_search_field = BlogSearchForm()

    # latest blogs
    latest_blogs = BlogModel.objects.select_related('author', 'blog_category').order_by('-created_at')[:3]

    context = {
        'pages': page_obj,
        'categories': category_list,
        'form': blog_search_field,
        'recent_blogs': latest_blogs,
    }

    return render(request, html_template_name, context)


def blog_search_functionality(request):

    html_template_name = 'blog/blog_search.html'

    get_keyword = BlogSearchForm(request.GET or None)
    result = BlogModel.objects.none()
    user_input = ''
    search_results = None

    if get_keyword.is_valid():
        user_input = get_keyword.cleaned_data.get('search_key')
        result = BlogModel.objects.filter(
            Q(title__icontains=user_input) | Q(blog_body__icontains=user_input)
        ).select_related('author', 'blog_category')

        paginator = Paginator(result, 6) 
        page_number = request.GET.get('page')
        search_results = paginator.get_page(page_number)

    context = {
        'pages': search_results,
        'keyword': user_input,
        'total_result': result,
    }

    return render(request, html_template_name, context)


@member_required
def blog_post_page(request):

    html_template_name = 'blog/blog_post.html'

    blog_post_form = BlogPostForm()

    context = {
        'form': blog_post_form,
    }

    return render(request, html_template_name, context)


@member_required
def publish_blog_view(request):

    current_user = request.user

    if request.method == 'POST':
        get_blog = BlogPostForm(request.POST, request.FILES)
        if get_blog.is_valid():
            saving_blog = get_blog.save(commit=False)
            saving_blog.author = current_user
            saving_blog.save()

    return redirect('blog:blog_page')


@member_required
def update_blog_view(request, blog_id):

    html_template_name = 'blog/blog_update.html'
    current_user = request.user

    if current_user.is_superuser or current_user.is_staff or getattr(current_user, 'role', None) == 'admin':
        instance = get_object_or_404(BlogModel, pk=blog_id)
    else:
        instance = get_object_or_404(BlogModel, pk=blog_id, author=current_user)

    if request.method == 'POST':
        update_blog = UpdateBlogForm(request.POST, request.FILES, instance=instance)
        if update_blog.is_valid():
            saving_blog = update_blog.save(commit=False)
            saving_blog.edited_at = datetime.datetime.now()
            saving_blog.save()
            return redirect('blog:blog_page')
    else:
        update_blog = UpdateBlogForm(instance=instance)

    context = {
        'form': update_blog,
        'blog_id_value': blog_id,
    }

    return render(request, html_template_name, context)


@member_required
def delete_blog_view(request, blog_id):

    current_user = request.user
    
    if current_user.is_superuser or current_user.is_staff or getattr(current_user, 'role', None) == 'admin':
        get_blog = get_object_or_404(BlogModel, pk=blog_id)
    else:
        get_blog = get_object_or_404(BlogModel, pk=blog_id, author=current_user)
    
    get_blog.delete()

    return redirect('blog:blog_page')


@login_required
def comment_adding_view(request, blog_id):

    get_blog = get_object_or_404(BlogModel, pk=blog_id)
    current_user = request.user

    if request.method == 'POST':
        get_comment = request.POST.get('comment', ' ').strip()
        get_comment = escape(get_comment)
    
        if len(get_comment) > 250: 
            return HttpResponse("Comment is too long!", status=400)

        # create comment entry
        BlogCommentModel.objects.create(
            user=current_user,
            blog=get_blog,
            comment=get_comment,
        )
        
        # update or create comment tracker
        tracker, created = BlogCommentTracker.objects.get_or_create(blog=get_blog)
        if not created:
            tracker.comment_count += 1
            tracker.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))