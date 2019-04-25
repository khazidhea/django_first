from django.http import HttpResponse
from django.shortcuts import render

from .models import Order, OrderItem


def hello(request):
    orders = Order.objects.filter(customer__user=request.user)
    return render(request, 'hello.html', context={
        'orders': orders
    })


def order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')
        try:
            quantity = int(quantity)
        except ValueError:
            return HttpResponse(
                'Quantity must be a positive int',
                status=400
            )
        if quantity <= 0:
            return HttpResponse(
                'Quantity must be a positive int',
                status=400
            )
        OrderItem.objects.create(
            order=order,
            product_id=product_id,
            quantity=int(quantity)
        )
    return render(request, 'order.html', context={
        'order': order
    })


def bye(request):
    return HttpResponse('Bye, world!')
