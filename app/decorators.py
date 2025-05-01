from django.shortcuts import redirect
from functools import wraps

def custom_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Check if the user is authenticated via your custom session method
        if request.session.get('user_id'):
            # If the user_id exists in the session, allow access to the view.
            return view_func(request, *args, **kwargs)
        else:
            # Otherwise, redirect the user to the login page.
            return redirect('login')
    return wrapper


