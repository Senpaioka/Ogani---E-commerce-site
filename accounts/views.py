from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from accounts.forms import RegistrationForm, UpdateUserInfo, ChangePasswordForm, ChangePictureForm
from accounts.models import UserAccount
from django.contrib.auth import update_session_auth_hash
from blog.models import BlogModel
from django.contrib.auth.decorators import login_required
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

        user = auth.authenticate(request, username=username, password=password)
        
        if user:
            auth.login(request, user)

            return redirect('home:home_page')



    context =  {}

    return render(request, html_template_name, context)










def logout_view(request):

    auth.logout(request)

    return redirect('home:home_page')











@login_required
def user_profile_page(request):

    html_template_name = 'accounts/profile.html'

    current_user = request.user

    if current_user.is_authenticated:
        user_info = UserAccount.objects.get(username=current_user)

        get_blogs = BlogModel.objects.filter(author=current_user).order_by('-edited_at')


    context = {
        'info': user_info,
        'user_blogs': get_blogs,
    }

    return render(request, html_template_name, context)











def user_update_page(request):

    html_template_name = 'accounts/update.html'

    # showing profile info
    current_user = request.user

    if current_user.is_authenticated: 
        instance = get_object_or_404(UserAccount, username=current_user)
           

        if request.method == 'POST':
            form = UpdateUserInfo(request.POST, instance=instance)

            if form.is_valid():
                
                update_form = form.save(commit=False)
                update_form.save()


        else:
            form = UpdateUserInfo(instance=instance) 

    context = {
        'form': form,
    }

    return render(request, html_template_name, context)






def user_settings_page(request):

    html_template_name = 'accounts/settings.html'

    current_user = request.user

    if current_user.is_authenticated:
        user_info = UserAccount.objects.get(username=current_user)

    context = {
        'info': user_info,
    }

    return render(request, html_template_name, context)





def change_password_page(request):

    html_template_name = 'accounts/change_password.html'

    current_user = request.user

    if current_user.is_authenticated: 
        instance = get_object_or_404(UserAccount, username=current_user)
           

        if request.method == 'POST':
            form = ChangePasswordForm(request.POST, instance=instance)

            if form.is_valid():
                
                update_form = form.save(commit=False)
                update_form.set_password(form.cleaned_data["confirm_password"])
                update_form.save()
                update_session_auth_hash(request, current_user)
                auth.logout(request)

                return redirect('account:login_page')


        else:
            form = ChangePasswordForm() 

    
    context = {
        'form': form,
    }

    return render(request, html_template_name, context)







def change_picture_page(request):

    html_template_name = 'accounts/change_picture.html'

    current_user = request.user

    if current_user.is_authenticated: 
        instance = get_object_or_404(UserAccount, username=current_user)
           

        if request.method == 'POST':
            form = ChangePictureForm(request.POST, request.FILES, instance=instance)

            if form.is_valid():
                form.save()
            
            return redirect('account:profile_page')

        else:
            form = ChangePictureForm()

    context = {
        'form': form,
    }

    return render(request, html_template_name, context)

