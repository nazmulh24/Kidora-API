from rest_framework import serializers

from order.models import Cart, CartItem
from product.models import Product


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price"]


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    total_price = serializers.SerializerMethodField(method_name="get_total_price")

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price", "line_total"]

    def get_total_price(self, cart_item: CartItem):
        return cart_item.product.price * cart_item.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    Total_Price = serializers.SerializerMethodField(method_name="get_total_price")

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "Total_Price"]
        read_only_fields = ["user"]

    def get_total_price(self, cart: Cart):
        list = sum([item.product.price * item.quantity for item in cart.items.all()])
        return list
