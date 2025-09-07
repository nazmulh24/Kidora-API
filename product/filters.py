from django_filters.rest_framework import FilterSet, NumberFilter

from product.models import Product


class ProductFilter(FilterSet):
    min_price = NumberFilter(field_name="stocks__price", lookup_expr="gte")
    max_price = NumberFilter(field_name="stocks__price", lookup_expr="lte")

    class Meta:
        model = Product
        fields = {"category_id": ["exact"]}
