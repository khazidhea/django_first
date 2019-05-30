from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import Order, OrderItem, Product, Customer
from .forms import OrderItemForm


def login_view(request):
    if request.user.is_authenticated:
        print('authenticated')
    if request.method == 'POST':
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponse('wrong username or password', status=401)
    return render(request, 'login.html')


def hello(request):
    products = Product.objects.all()
    return render(request, 'hello.html', context={
        'products': products
    })


def order_list(request):
    if request.method == 'POST':
        customer = Customer.objects.get(user=request.user)
        location = request.POST.get('location')
        Order.objects.create(
            customer=customer,
            location=location
        )
    orders = Order.objects.filter(customer__user=request.user)
    return render(request, 'orders.html', context={
        'orders': orders
    })


def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product']
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return HttpResponse(
                    'Product not found',
                    status=404
                )
            quantity = form.cleaned_data['quantity']
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )
        else:
            return HttpResponse('Validation error', status=400)
    else:
        form = OrderItemForm()
    return render(request, 'order.html', context={
        'order': order,
        'form': form
    })


def bye(request):
    return HttpResponse('Bye, world!')
