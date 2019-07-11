from django.contrib import admin

from .models import (
    Attribute, AttributeValue, Product, Store, StoreItem, Order, OrderItem
)


class SizeFilter(admin.SimpleListFilter):
    title = 'Size'
    parameter_name = 'size'

    def lookups(self, request, model_admin):
        size = Attribute.objects.get(name='size')
        values = size.values.all()
        return (
            (value.value, value.value) for value in values
        )

    def queryset(self, request, queryset):
        if self.value():
            value = AttributeValue.objects.get(value=self.value())
            queryset = queryset.filter(attributes__in=[value])
        return queryset


class ColorFilter(admin.SimpleListFilter):
    title = 'Color'
    parameter_name = 'color'

    def lookups(self, request, model_admin):
        color = Attribute.objects.get(name='color')
        values = color.values.all()
        return (
            (value.value, value.value) for value in values
        )

    def queryset(self, request, queryset):
        if self.value():
            value = AttributeValue.objects.get(value=self.value())
            queryset = queryset.filter(attributes__in=[value])
        return queryset


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    list_filter = ('category', SizeFilter, ColorFilter)


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
