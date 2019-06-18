from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from .models import Order, OrderItem, Product, Customer
from .forms import OrderItemForm


class HomeView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'home.html'


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'orders.html'

    def get_queryset(self):
        return Order.objects.filter(customer__user=self.request.user)

    def post(self, request):
        customer = Customer.objects.get(user=request.user)
        location = request.POST.get('location', 'Almaty')
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        order = Order.objects.create(
            customer=customer,
            location=location
        )
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1
        )
        return HttpResponseRedirect('/orders/{}'.format(order.id))


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
