from django.shortcuts import render

# Create your views here.

def blog_page(request):

    html_template_name = 'blog/blog.html'

    context = {}

    return render(request, html_template_name, context)


