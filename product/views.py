from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from api.permissions import IsAdminOrReadOnly

from product.paginations import DefaultPagination
from product.filters import ProductFilter
from product.models import Category, Product
from product.serializers import CategorySerializer, ProductSerializer

from django.db.models import Count


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(product_count=Count("products")).all()
    serializer_class = CategorySerializer

    permission_classes = [IsAdminOrReadOnly]


class ProductViewSet(ModelViewSet):
    """
    API endpoint for managing products in the e-commerce store
     - Allows authenticated admin to create, update, and delete products
     - Allows users to browse and filter product
     - Support searching by name, description, and category
     - Support ordering by price and updated_at
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["price"]

    def list(self, request, *args, **kwargs):
        """Retrive all the products"""
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Only authenticated admin can create product"""
        return super().create(request, *args, **kwargs)
