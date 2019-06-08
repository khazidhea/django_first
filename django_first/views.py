from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.views.generic.base import TemplateView

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


class HelloView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'hello.html'


class OrderListView(ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'orders.html'

    def get_queryset(self):
        return Order.objects.filter(customer__user=self.request.user)

    def post(self, request):
        customer = Customer.objects.get(user=request.user)
        location = request.POST.get('location')
        Order.objects.create(
            customer=customer,
            location=location
        )
        return self.get(request)


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


class ByeView(TemplateView):
    template_name = 'bye.html'
