from urllib.parse import urlencode, urlparse, urlunparse, parse_qs

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, UpdateView
from django.views.generic.base import TemplateView

from .models import Order, OrderItem, Product, Customer, Category
from .forms import OrderForm, OrderItemForm, OrderItemFormSet


class HomeView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'home.html'

    @staticmethod
    def _filter_url(current_url, filter_name, filter_value):
        """
        Adds filtre value to current url
        """
        u = urlparse(current_url)
        query = parse_qs(u.query)
        query[filter_name] = filter_value
        u = u._replace(query=urlencode(query, True))
        url = urlunparse(u)
        return url

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all()

        category = self.request.GET.get('category')
        if category:
            try:
                category = Category.objects.get(name=category)
                url = self.request.get_full_path()
                filters = {
                    attribute.name: attribute.values.all()
                    for attribute in category.attributes.all()
                }

                for name, values in filters.items():
                    filters[name] = [
                        {
                            'url': HomeView._filter_url(url, name, value),
                            'name': value.value
                        } for value in values
                    ]
                context['filters'] = filters
            except Category.DoesNotExist:
                pass
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        category_filter = self.request.GET.get('category')
        if category_filter:
            try:
                category = Category.objects.get(name=category_filter)
            except Category.DoesNotExist:
                return []
            queryset = queryset.filter(category=category)

            filter_params = {
                param: value
                for param, value in self.request.GET.items()
                if not param == 'category'
            }
            for filter_name, filter_value in filter_params.items():
                attribute = category.attributes.get(name=filter_name)
                value = attribute.values.filter(value=filter_value)
                queryset = queryset.filter(attributes__in=value)
        return queryset


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


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    context_object_name = 'order'
    template_name = 'order.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        print(self.object)
        if self.request.POST:
            context['items'] = OrderItemFormSet(self.request.POST)
        else:
            context['items'] = OrderItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['items']
        if formset.is_valid():
            print('valid')
            formset.instance = self.object
            formset.save()
            for f in formset: 
                cd = f.cleaned_data
                print(cd)
            return super().form_valid(form)
        else:
            print(formset.errors)
            print(formset.total_error_count())
            return super().form_invalid(form)


def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    form = None
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
    return render(request, 'order.html', context={
        'order': order,
        'form': form,
        'items': OrderItemFormSet(instance=order)
    })


class ByeView(TemplateView):
    template_name = 'bye.html'
