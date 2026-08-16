from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from apps.accounts.models import RoleChoices, UserAccount


class CustomAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return True

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        user.is_active = True
        if isinstance(user, UserAccount) or hasattr(user, 'role'):
            if not getattr(user, 'role', None):
                setattr(user, 'role', RoleChoices.USER)
        if commit:
            user.save()
        return user


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        # Set default role if model supports it
        if hasattr(user, 'role'):
            user.role = RoleChoices.USER

        # Ensure first_name and last_name are populated if available
        if not user.first_name:
            user.first_name = data.get('first_name') or data.get('given_name') or ''
        if not user.last_name:
            user.last_name = data.get('last_name') or data.get('family_name') or ''

        # Fallback values for required non-nullable fields in UserAccount model
        if hasattr(user, 'city') and not user.city:
            user.city = 'N/A'
        if hasattr(user, 'country') and not user.country:
            user.country = 'N/A'

        # Ensure unique username logic fallback
        if not user.username:
            email_prefix = user.email.split('@')[0] if user.email else 'user'
            base_username = email_prefix[:15]
            username = base_username
            counter = 1
            while UserAccount.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            user.username = username

        # Ensure user is active upon creation
        user.is_active = True

        return user

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form=form)
        user.is_active = True
        if hasattr(user, 'role'):
            user.role = RoleChoices.USER
        user.save()
        return user

    def is_auto_signup_allowed(self, request, sociallogin):
        return True

