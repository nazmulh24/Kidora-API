from rest_framework import serializers
from decimal import Decimal
from product.models import Category, Product, ProductImage, Review, ReviewImage

from django.contrib.auth import get_user_model


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "product_count"]

    product_count = serializers.IntegerField(
        read_only=True, help_text="Number of products in this category"
    )


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = ProductImage
        fields = ["id", "image"]


class ProductSerializer(serializers.ModelSerializer):
    total_reviews = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "size",
            "price",
            "is_in_stock",
            "stock",
            "category",
            "price_with_tax",
            "total_reviews",
            "average_rating",
            "images",
            "video_url",
        ]

    def get_total_reviews(self, obj):
        return obj.total_reviews()

    def get_average_rating(self, obj):
        return obj.average_rating()

    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    # --> 15% tax
    def calculate_tax(self, product):
        return round(product.price * Decimal(1.15), 2)

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError("Price could't be negative !")
        return price


class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name="full_name")

    class Meta:
        model = get_user_model()
        fields = ["id", "name"]

    def full_name(self, obj):
        return obj.get_full_name()


class ReviewImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = ReviewImage
        fields = ["id", "image"]


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name="get_user")
    images = ReviewImageSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ["id", "user", "product", "rating", "comment", "images"]
        read_only_fields = ["user", "product"]

    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data

    def create(self, validated_data):
        product_id = self.context["product_id"]
        review = Review.objects.create(product_id=product_id, **validated_data)
        return review
