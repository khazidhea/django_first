from rest_framework.viewsets import ModelViewSet
from rest_framework import routers

from .models import Category, Order
from .serializers import (
    CategorySerializer, CategoryDetailSerializer,
    OrderSerializer, OrderDetailSerializer, OrderCreateSerializer
)


class MultiSerializerViewSetMixin(object):
    def get_serializer_class(self):
        """
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:

        class MyViewSet(MultiSerializerViewSetMixin, ViewSet):
            serializer_class = MyDefaultSerializer
            serializer_action_classes = {
               'list': MyListSerializer,
               'my_action': MyActionSerializer,
            }

            @action
            def my_action:
                ...

        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class, DefaultSerializer.

        """
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(MultiSerializerViewSetMixin, self).get_serializer_class()


class CategoryViewSet(MultiSerializerViewSetMixin, ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    serializer_action_classes = {
        'list': CategorySerializer,
        'retrieve': CategoryDetailSerializer,
    }



class OrderViewSet(MultiSerializerViewSetMixin, ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    serializer_action_classes = {
        'list': OrderSerializer,
        'retrieve': OrderDetailSerializer,
        'create': OrderCreateSerializer
    }


router = routers.SimpleRouter()
router.register('categories', CategoryViewSet)
router.register('orders', OrderViewSet)
api_urls = router.urls
