from django import forms
from contact.models import ContactFormModel, NewsLetterModel


class ContactForm(forms.ModelForm):

    class Meta:
        model = ContactFormModel
        fields = ['name', 'email', 'message_body']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['message_body'].required = True


    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Your Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Your Email'
        self.fields['message_body'].widget.attrs['placeholder'] = 'Your Message'





class NewsLetterForm(forms.ModelForm):

    class Meta:
        model = NewsLetterModel
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    def __init__(self, *args, **kwargs):
        super(NewsLetterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Your Email'