from django import forms
from accounts.models import UserAccount


class RegistrationForm(forms.ModelForm):

    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
    }))

    confirm_password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'placeholder': 'Password confirmation'
    }))



    class Meta:
        model = UserAccount
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'address', 'city', 'country', 'birth_date']




    def clean(self):

        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:

            raise forms.ValidationError(
                "Password does not match!"
            )
        
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Your First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Your last Name'
        self.fields['username'].widget.attrs['placeholder'] = 'Provide Unique Username'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Unique Email Address'
        self.fields['phone'].widget.attrs['placeholder'] = 'Your Phone Number'
        self.fields['address'].widget.attrs['placeholder'] = 'Your Shipping Address'
        self.fields['city'].widget.attrs['placeholder'] = 'City You Live In'
        self.fields['country'].widget.attrs['placeholder'] = 'Country Name'
        self.fields['birth_date'].widget.attrs['placeholder'] = 'Your Birth Date'