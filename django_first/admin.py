from django.contrib import admin

from .models import Product, Store, StoreItem, Order, OrderItem


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')


class StoreItemInline(admin.TabularInline):
    model = StoreItem
    extra = 0


class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'location')
    inlines = (StoreItemInline,)


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'location')
    inlines = (OrderItemInline,)


admin.site.register(Product, ProductAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Order, OrderAdmin)
