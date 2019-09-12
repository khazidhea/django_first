from rest_framework.viewsets import ModelViewSet
from rest_framework import routers

from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


router = routers.SimpleRouter()
router.register(r'categories', CategoryViewSet)
api_urls = router.urls
