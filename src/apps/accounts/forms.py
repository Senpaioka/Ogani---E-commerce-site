from django import forms
from django.contrib.auth.password_validation import validate_password
from apps.accounts.models import UserAccount


class RegistrationForm(forms.ModelForm):

    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
    }))

    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={
        'placeholder': 'Password confirmation'
    }))

    class Meta:
        model = UserAccount
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'address', 'city', 'country', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}), 
        }

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data:
            return cleaned_data

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Password does not match!")

        if password:
            try:
                validate_password(password)
            except forms.ValidationError as error:
                self.add_error('password', error)

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Your First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Your last Name'
        self.fields['username'].widget.attrs['placeholder'] = 'Provide Unique Username'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Unique Email Address'
        self.fields['phone'].widget.attrs['placeholder'] = 'Your Phone Number'
        self.fields['address'].widget.attrs['placeholder'] = 'Your Shipping Address'
        self.fields['city'].widget.attrs['placeholder'] = 'City You Live In'
        self.fields['country'].widget.attrs['placeholder'] = 'Country Name'
        self.fields['birth_date'].widget.attrs['placeholder'] = 'Your Birth Date'


class UpdateUserInfo(forms.ModelForm):

    class Meta:
        model = UserAccount
        exclude = ['password', 'confirm_password', 'is_active', 'is_staff', 'is_admin', 'is_superuser', 'groups', 'user_permissions'] 
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}), 
        }


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Current Password'})
    )
    password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter New Password'})
    )
    confirm_password = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'})
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if self.user and not self.user.check_password(old_password):
            raise forms.ValidationError("Current password is incorrect.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data:
            return cleaned_data

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "New passwords do not match!")

        if password and self.user:
            try:
                validate_password(password, user=self.user)
            except forms.ValidationError as error:
                self.add_error('password', error)

        return cleaned_data


class ChangePictureForm(forms.ModelForm):

    class Meta:
        model = UserAccount
        fields = ['profile_picture']






# using RegistrationForm
class ChangePictureForm(forms.ModelForm):

    class Meta:
        model = UserAccount
        fields = ['profile_picture']