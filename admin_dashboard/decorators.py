from django.shortcuts import render
from functools import wraps

def admin_only(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
        return render(request, '404.html', status=404)
    return wrapper

def is_admin_or_teacher(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role in ['admin', 'teacher']:
            return view_func(request, *args, **kwargs)
        return render(request, '404.html', status=404)
    return wrapper




