from django.shortcuts import render

# Create your views here.

def registration_page(request):

    html_template_name = 'account/register.html'

    context =  {}

    return render(request, html_template_name, context)



def login_page(request):

    html_template_name = 'account/login.html'

    context =  {}

    return render(request, html_template_name, context)