from django.shortcuts import render, redirect
from contact.models import ContactInfoModel
from contact.contact_form import ContactForm, NewsLetterForm

# Create your views here.


def contact_page_view(request):

    html_template_name = 'contact\contact.html'

    contact_info = ContactInfoModel.objects.all()[0]

    contact_form = ContactForm()

    context = {
        'contact': contact_info,
        'form': contact_form,
    }

    return render(request, html_template_name, context)







def contact_message_save(request):

    current_user = request.user

    if current_user.is_authenticated:

        if request.method == 'POST':

            get_contact_form = ContactForm(request.POST)

            if get_contact_form.is_valid():
                get_contact_form.cleaned_data.get('name')
                get_contact_form.cleaned_data.get('email')
                get_contact_form.cleaned_data.get('message_body')

                get_contact_form.save()

    else:

        get_contact_form = ContactForm()

    return redirect('contact:contact_page')




# newsletter functionality
def subscribe_user_from_newsletter(request):

    if request.method == 'POST':
        get_newsletter_form = NewsLetterForm(request.POST)

        if get_newsletter_form.is_valid():
            get_newsletter_form.cleaned_data.get('email')
            get_newsletter_form.save()

    return redirect('home:home_page')





