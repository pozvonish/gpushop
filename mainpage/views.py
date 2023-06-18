from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic import CreateView
from .forms import RegisterUserForm, AuthenticationUserForm
from products.models import *
from orders.models import *
from django.shortcuts import redirect

def mainpage(request):
    return render(request, 'mainpage/mainpage.html', locals())

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'auth/register.html'
    success_url = 'login'

class LoginUser(LoginView):
    form_class = AuthenticationUserForm
    template_name = 'auth/login.html'
    def get_success_url(self):
        return '/'

def logout_user(request):
    logout(request)
    return redirect('login')

def orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
        reversed_orders = reversed(orders)
        return render(request, 'auth/orders.html', locals())
    else:
        return redirect('login')

def order(request, order_id):
    if request.user.is_authenticated:
        order = Order.objects.get(id=order_id)
        if order.user == request.user:
            products_in_order=ProductInOrder.objects.filter(order=order_id)
            return render(request, 'auth/order.html', locals())
        else:
            return redirect('/')
    else:
        return redirect('login')
