from django.http import HttpResponse
from django.shortcuts import render

from .models import Order, OrderItem, Product


def hello(request):
    orders = Order.objects.filter(customer__user=request.user)
    return render(request, 'hello.html', context={
        'orders': orders
    })


def order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        product_id = request.POST.get('product')
        try:
            product_id = int(product_id)
        except ValueError:
            return HttpResponse(
                'Invalid product id',
                status=400
            )
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return HttpResponse(
                'Product not found',
                status=404
            )
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
            product=product,
            quantity=int(quantity)
        )
    return render(request, 'order.html', context={
        'order': order
    })


def bye(request):
    return HttpResponse('Bye, world!')
