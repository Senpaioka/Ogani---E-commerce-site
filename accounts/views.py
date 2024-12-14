from django.shortcuts import render, redirect
from django.contrib import auth
from accounts.forms import RegistrationForm
from accounts.models import UserAccount

# Create your views here.

def registration_page(request):

    html_template_name = 'accounts/register.html'

    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)

        if registration_form.is_valid():
            # required fields
            first_name = registration_form.cleaned_data['first_name']
            last_name = registration_form.cleaned_data['last_name']
            username = registration_form.cleaned_data['username']
            email = registration_form.cleaned_data['email']
            city = registration_form.cleaned_data['city']
            country = registration_form.cleaned_data['country']
            password = registration_form.cleaned_data['password']

            # other fields
            address = registration_form.cleaned_data['address']
            phone = registration_form.cleaned_data['phone']
            birth_date = registration_form.cleaned_data['birth_date']

            # saving all data
            user = UserAccount.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, city=city, country=country, password=password)
            user.address = address
            user.phone = phone
            user.birth_date = birth_date
            user.save()

            return redirect('account:login_page')
    else:
        registration_form = RegistrationForm()





    context =  {
        'form': registration_form,
    }

    return render(request, html_template_name, context)












def login_page(request):

    html_template_name = 'accounts/login.html'

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        
        if user:
            return redirect('home:home_page')



    context =  {}

    return render(request, html_template_name, context)