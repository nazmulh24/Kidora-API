from rest_framework import serializers
from decimal import Decimal
from product.models import (
    Category,
    Product,
    ProductStock,
    ProductImage,
    Review,
    ReviewImage,
)
from order.models import Wishlist

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


class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStock
        fields = ["id", "size", "price", "stock"]


class ProductSerializer(serializers.ModelSerializer):
    total_reviews = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, required=False)
    is_in_wishlist = serializers.SerializerMethodField()
    stocks = ProductStockSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "stocks",
            "is_in_stock",
            "total_stock",
            "category",
            "total_reviews",
            "average_rating",
            "images",
            "video_url",
            "is_in_wishlist",
        ]

    def get_is_in_wishlist(self, obj):
        user = self.context.get("request").user if self.context.get("request") else None
        if user and user.is_authenticated:
            return Wishlist.objects.filter(user=user, products=obj).exists()
        return False

    def create(self, validated_data):
        images_data = validated_data.pop("images", [])
        stocks_data = validated_data.pop("stocks", [])
        product = Product.objects.create(**validated_data)
        for stock_data in stocks_data:
            ProductStock.objects.create(product=product, **stock_data)
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)
        return product

    def get_total_reviews(self, obj):
        return obj.total_reviews()

    def get_average_rating(self, obj):
        return obj.average_rating()

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
    images = ReviewImageSerializer(many=True, required=False)

    class Meta:
        model = Review
        fields = ["id", "user", "product", "rating", "comment", "images"]
        read_only_fields = ["user", "product"]

    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data

    def create(self, validated_data):
        images_data = validated_data.pop("images", [])
        product_id = self.context["product_id"]
        review = Review.objects.create(product_id=product_id, **validated_data)
        for image_data in images_data:
            ReviewImage.objects.create(review=review, **image_data)
        return review
