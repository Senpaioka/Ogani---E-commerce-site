from contact.contact_form import NewsLetterForm

def newsletter_for_all_app(request):

    return {'newsletter_form': NewsLetterForm()}