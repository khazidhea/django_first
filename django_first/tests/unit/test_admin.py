from django_first.admin import ColorFilter, SizeFilter, ProductAdmin
from django_first.models import Product


def test_size_filter(db, data):
    size_filter = SizeFilter(None, {'size': 'small'}, Product, ProductAdmin)
    lookups = list(size_filter.lookups(None, ProductAdmin))
    assert len(lookups) == 3
    assert ('small', 'small') in lookups
    assert ('medium', 'medium') in lookups
    assert ('large', 'large') in lookups

    queryset = size_filter.queryset(None, Product.objects.all())
    assert len(queryset) == 1
    product = queryset[0]
    assert product.name == 'apple'
    attributes = [attribute.value for attribute in product.attributes.all()]
    assert 'small' in attributes


def test_color_filter(db, data):
    color_filter = ColorFilter(
        None, {'color': 'yellow'}, Product, ProductAdmin
    )
    lookups = list(color_filter.lookups(None, ProductAdmin))
    assert len(lookups) == 2
    assert ('green', 'green') in lookups
    assert ('yellow', 'yellow') in lookups

    queryset = color_filter.queryset(None, Product.objects.all())
    assert len(queryset) == 1
    product = queryset[0]
    assert product.name == 'banana'
    attributes = [attribute.value for attribute in product.attributes.all()]
    assert 'yellow' in attributes
