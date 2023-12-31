from django.http import HttpResponse
from django.shortcuts import redirect
from accounts.models import Customer


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('customerhome')
        else:
            return view_func(request, *args, **kwargs)

    wrapper_func.__name__ = view_func.__name__  # Preserve the original function name
    return wrapper_func


def authenticated_useronly(view_func):
	def wrapper_func(request,*args,**kwargs):
		if(not request.user.is_authenticated):
			return redirect('login')
		else:
			return view_func(request,*args,**kwargs)
	return wrapper_func

def loginlogoutdecorator(view_func):
	def wrapper_func(request,*args,**kwargs):
		if(request.user.is_authenticated):
			return  redirect('customerhome')
		
		if(not request.user.is_authenticated):
			return view_func(request,*args,**kwargs)
		
		return HttpResponse('There is something wrong go back')
	return  wrapper_func
			

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You are not authorized to view this page')
		return wrapper_func
	return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('user-page')

        if request.user.is_superuser:  # Added condition for superuser
            return view_func(request, *args, **kwargs)
        
        return HttpResponse('You are not authorized to view this page')

    return wrapper_function




		


    
	
		

		
		
