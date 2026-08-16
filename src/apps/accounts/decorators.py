from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.contrib import messages

def role_required(allowed_roles=None):
    """
    Decorator for views that checks whether a user has a specific role.
    Allowed roles can be passed as strings, e.g. ['member', 'admin'].
    """
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('account:login_page')
            
            # Superusers and staff have administrative access
            if request.user.is_superuser or request.user.is_staff or getattr(request.user, 'role', None) in allowed_roles:
                return view_func(request, *args, **kwargs)
            
            messages.error(request, "Permission Denied: You do not have permission to access this page.")
            return render(request, '403.html', status=403)
        return _wrapped_view
    return decorator


def member_required(view_func):
    """
    Decorator for views requiring member or admin role (e.g., posting blogs).
    """
    return role_required(['member', 'admin'])(view_func)


def admin_required(view_func):
    """
    Decorator for views requiring admin role.
    """
    return role_required(['admin'])(view_func)
