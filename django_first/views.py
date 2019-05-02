from django.http import HttpResponse
from django.shortcuts import render

from .models import Order, OrderItem, Product, Customer
from .forms import OrderItemForm


def hello(request):
    if request.method == 'POST':
        customer = Customer.objects.get(user=request.user)
        location = request.POST.get('location')
        Order.objects.create(
            customer=customer,
            location=location
        )
    orders = Order.objects.filter(customer__user=request.user)
    print(orders[0].id)
    return render(request, 'hello.html', context={
        'orders': orders
    })


def order(request, order_id):
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
