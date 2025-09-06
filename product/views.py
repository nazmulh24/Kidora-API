from rest_framework.viewsets import ModelViewSet
from api.permissions import IsAdminOrReadOnly

from product.models import Category
from product.serializers import CategorySerializer

from django.db.models import Count


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(product_count=Count("products")).all()
    serializer_class = CategorySerializer

    permission_classes = [IsAdminOrReadOnly]
