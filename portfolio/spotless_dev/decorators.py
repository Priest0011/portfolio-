# Only create this if you don't already have a working decorators.py
from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.urls import reverse


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        return redirect_to_login(request.get_full_path(), login_url=reverse("admin_login"))

    return _wrapped
 