from django.shortcuts import render

# Create your views here.

def home_view(request):

    html_file_name = 'home/home.html'

    context = {}

    return render(request, html_file_name, context)