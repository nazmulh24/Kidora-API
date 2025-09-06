from rest_framework import serializers
from decimal import Decimal
from product.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "product_count"]

    product_count = serializers.IntegerField(
        read_only=True, help_text="Number of products in this category"
    )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "is_in_stock",
            "stock",
            "category",
            "price_with_tax",
            "image",
        ]

    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    # --> 15% tax
    def calculate_tax(self, product):
        return round(product.price * Decimal(1.15), 2)

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError("Price could't be negative !")
        return price
