from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from apps.accounts.forms import (
    RegistrationForm, 
    UpdateUserInfo, 
    ChangePasswordForm, 
    ChangePictureForm
)
from apps.accounts.models import UserAccount
from apps.blog.models import BlogModel


def registration_page(request):
    html_template_name = 'accounts/register.html'

    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)

        if registration_form.is_valid():
            # Required fields
            first_name = registration_form.cleaned_data['first_name']
            last_name = registration_form.cleaned_data['last_name']
            username = registration_form.cleaned_data['username']
            email = registration_form.cleaned_data['email']
            city = registration_form.cleaned_data['city']
            country = registration_form.cleaned_data['country']
            password = registration_form.cleaned_data['password']

            # Other fields
            address = registration_form.cleaned_data['address']
            phone = registration_form.cleaned_data['phone']
            birth_date = registration_form.cleaned_data['birth_date']

            # Saving user
            user = UserAccount.objects.create_user(
                first_name=first_name, 
                last_name=last_name, 
                username=username, 
                email=email, 
                city=city, 
                country=country, 
                password=password
            )
            user.address = address
            user.phone = phone
            user.birth_date = birth_date
            user.save()

            return redirect('account:login_page')
    else:
        registration_form = RegistrationForm()

    context = {
        'form': registration_form,
    }

    return render(request, html_template_name, context)


def login_page(request):
    html_template_name = 'accounts/login.html'
    error_message = None
    next_url = request.POST.get('next') or request.GET.get('next', '')

    if request.user.is_authenticated:
        return redirect('home:home_page')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                if next_url:
                    return redirect(next_url)
                return redirect('home:home_page')
            else:
                error_message = 'Account is disabled.'
        else:
            error_message = 'Invalid username or password.'

    context = {
        'error_message': error_message,
        'next': next_url,
    }
    return render(request, html_template_name, context)


def logout_view(request):
    auth.logout(request)
    return redirect('home:home_page')


@login_required
def user_profile_page(request):
    html_template_name = 'accounts/profile.html'

    # Direct access to request.user without extra DB lookup
    # select_related prevents N+1 query when iterating over blogs in template
    get_blogs = BlogModel.objects.filter(author=request.user).select_related('author').order_by('-edited_at')

    context = {
        'info': request.user,
        'user_blogs': get_blogs,
    }

    return render(request, html_template_name, context)


@login_required
def user_update_page(request):
    html_template_name = 'accounts/update.html'
    instance = request.user

    if request.method == 'POST':
        form = UpdateUserInfo(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('account:profile_page')
    else:
        form = UpdateUserInfo(instance=instance)

    context = {
        'form': form,
    }

    return render(request, html_template_name, context)


@login_required
def user_settings_page(request):
    html_template_name = 'accounts/settings.html'

    context = {
        'info': request.user,
    }

    return render(request, html_template_name, context)


@login_required
def change_password_page(request):
    html_template_name = 'accounts/change_password.html'

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            new_password = form.cleaned_data['password']
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            return redirect('account:profile_page')
    else:
        form = ChangePasswordForm(user=request.user)

    context = {
        'form': form,
    }

    return render(request, html_template_name, context)


@login_required
def change_picture_page(request):
    html_template_name = 'accounts/change_picture.html'
    instance = request.user

    if request.method == 'POST':
        form = ChangePictureForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('account:profile_page')
    else:
        form = ChangePictureForm(instance=instance)

    context = {
        'form': form,
    }

    return render(request, html_template_name, context)
