from django.http import HttpResponse
from django.shortcuts import render

from .models import Order


def hello(request):
    orders = Order.objects.filter(customer__user=request.user)
    return render(request, 'hello.html', context={
        'orders': orders
    })


def order(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order.html', context={
        'order': order
    })


def bye(request):
    return HttpResponse('Bye, world!')
