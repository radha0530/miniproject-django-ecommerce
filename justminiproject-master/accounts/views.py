from django.shortcuts import render, redirect 
from django.forms import inlineformset_factory

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from core.models import OrderItem,OrderModel


import random
import string


# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only,loginlogoutdecorator








def generate_random_string():
	letters = string.ascii_letters
	return ''.join(random.choice(letters) for _ in range(6))








def send_verification_email(user_email, verification_code):
    subject = 'Email Verification'
    template = 'accounts/verification_email.html'
    context = {'verification_code': verification_code}
    email_body = render_to_string(template, context)
    from_email = 'jamesharrypotter8@gmail.com'  # Update with your email address
    recipient_list = [user_email]

    send_mail(subject, '', from_email, recipient_list, html_message=email_body)





@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            verification_code = generate_random_string()
            customer = Customer.objects.create(
                user=user,
                name=user.username,
                email=email,
                verification_code=verification_code
            )
            customer.user_id = user.id  # Set the user_id field
            customer.save()
            serialized_user = serializers.serialize('json', [user])
            request.session['user']=serialized_user
            login(request,user)

            send_verification_email(email, verification_code)
            return redirect('verification')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@loginlogoutdecorator
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        next_url = request.GET.get('next')

        if user is not None:
            if hasattr(user, 'customer'):
                # User has a related Customer object
                customer_email_status = user.customer.email_verified
            else:
                # Create a Customer instance for the user
                customer = Customer.objects.create(user=user)
                customer_email_status = False

            if customer_email_status or user.is_superuser:
                login(request, user)
                if next_url:
                    # Redirect the user to the URL specified in the 'next' parameter
                    return redirect(next_url)
                return redirect('customerhome')
            else:
                
                # Return an HttpResponse object instead of using messages framework
                return render(request, 'accounts/login.html', {'error': 'Your email is not verified.'})

        else:
            # Return an HttpResponse object instead of using messages framework
            return render(request, 'accounts/login.html', {'error': 'Invalid username or password.'})

    return render(request, 'accounts/login.html')

def logoutUser(request):
	logout(request)
	return redirect('customerhome')

@login_required(login_url='login')
@admin_only
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	Sampai = orders.filter(status='Sampai').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders':orders, 'customers':customers,
	'total_orders':total_orders,'Sampai':Sampai,
	'pending':pending }

	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer.order_set.all()

	total_orders = orders.count()
	Sampai = orders.filter(status='Sampai').count()
	pending = orders.filter(status='Pending').count()

	print('ORDERS:', orders)

	context = {'orders':orders, 'total_orders':total_orders,
	'Sampai':Sampai,'pending':pending}
	return render(request, 'accounts/user.html', context)


@login_required(login_url='login')

def products(request):
	products = Product.objects.all()

	return render(request, 'accounts/products.html', {'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs 

	context = {'customer':customer, 'orders':orders, 'order_count':order_count,
	'myFilter':myFilter}
	return render(request, 'accounts/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'accounts/delete.html', context)


def customerhome(request):
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        
        if customer and not customer.email_verified:
            logout(request)
        else:
            return render(request, 'accounts/customerhome.html')

    return render(request, 'accounts/customerhome.html')
          
    

            
              
        
          
    
        
    
          

    return render(request, "accounts/customerhome.html")






# views.py


def verify_email(request):
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        print("verification_Code", verification_code)
	
        
        try:
            


	    
            customer = Customer.objects.get(user_id=request.user.id,verification_code=verification_code,email_verified=False)
            print( customer.verification_code == verification_code)
            if customer.verification_code == verification_code:
                
                customer.email_verified = True
                customer.save()
               
                
                
                return render(request, 'accounts/verification_success.html')
                
	            
            else:
                
                return redirect(request, 'accounts/verification_fail.html')
            
        except ObjectDoesNotExist:
            return render(request, 'accounts/verification_fail.html')

    return render(request, 'accounts/verification_form.html')




def navbar(request):
    cart_count = 0

    if request.user.is_authenticated:
        order_items = OrderItem.objects.filter(user=request.user)
        cart_count = order_items.count()

    context = {
        'cart_count': cart_count
    }

    return render(request, 'accounts/navbarmain.html', context)