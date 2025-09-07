from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from api.permissions import IsAdminOrReadOnly

from product.permissions import IsReviewAuthorOrReadonly
from product.paginations import DefaultPagination
from product.filters import ProductFilter
from product.models import Category, Product, Review
from product.serializers import CategorySerializer, ProductSerializer, ReviewSerializer

from order.models import Wishlist
from order.serializers import WishlistProductSerializer

from django.db.models import Count


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(product_count=Count("products")).all()
    serializer_class = CategorySerializer

    permission_classes = [IsAdminOrReadOnly]


class EmptySerializer(serializers.Serializer):
    class Meta:
        ref_name = "ProductEmptySerializer"
    pass


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

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        serializer_class=EmptySerializer,
    )
    def add_to_wishlist(self, request, pk=None):
        """Add this product to the authenticated user's wishlist."""
        product = self.get_object()
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        if wishlist.products.filter(pk=product.pk).exists():
            return Response(
                {"success": False, "message": "Product already in wishlist."},
                status=200,
            )
        wishlist.products.add(product)
        return Response(
            {"success": True, "message": "Product added to wishlist."}, status=201
        )

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        serializer_class=EmptySerializer,
    )
    def remove_from_wishlist(self, request, pk=None):
        """Remove this product from the authenticated user's wishlist."""
        product = self.get_object()
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        if not wishlist.products.filter(pk=product.pk).exists():
            return Response(
                {"success": False, "message": "Product not in wishlist."}, status=200
            )
        wishlist.products.remove(product)
        return Response(
            {"success": True, "message": "Product removed from wishlist."}, status=200
        )

    def get_wishlist_response(self, wishlist):
        products = wishlist.products.all()
        serializer = WishlistProductSerializer(products, many=True)
        return Response(serializer.data)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadonly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs.get("product_pk"))

    def get_serializer_context(self):
        return {"product_id": self.kwargs.get("product_pk")}
