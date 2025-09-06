from rest_framework import serializers
from decimal import Decimal
from product.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "product_count"]

    product_count = serializers.IntegerField(
        read_only=True, help_text="Number of products in this category"
    )
