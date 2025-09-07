from rest_framework import serializers

from order.services import OrderService
from order.models import Cart, CartItem, Order, OrderItem, Wishlist
from product.models import Product, ProductStock


class EmptySerializer(serializers.Serializer):
    class Meta:
        ref_name = "OrderEmptySerializer"

    pass


class SimpleProductSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "price"]

    def get_price(self, product: Product):
        first_stock = product.stocks.first()
        if first_stock:
            return first_stock.price
        return None


class AddCartItemSerializer(serializers.ModelSerializer):
    product_stock_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ["id", "product_stock_id", "quantity"]

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_stock_id = self.validated_data["product_stock_id"]
        quantity = self.validated_data["quantity"]

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_stock_id=product_stock_id
            )
            cart_item.quantity += quantity
            self.instance = cart_item.save()
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data
            )
        return self.instance

    def validate_product_stock_id(self, value):
        if not ProductStock.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                f"ProductStock with id:{value} does't exists."
            )
        return value


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]


class CartItemSerializer(serializers.ModelSerializer):
    product_stock = SimpleProductSerializer(source="product_stock.product")

    total_price = serializers.SerializerMethodField(method_name="get_total_price")

    class Meta:
        model = CartItem
        fields = ["id", "product_stock", "quantity", "total_price"]

    def get_total_price(self, cart_item: CartItem):
        return cart_item.product_stock.price * cart_item.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    Total_Price = serializers.SerializerMethodField(method_name="get_total_price")

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "Total_Price"]
        read_only_fields = ["user"]

    def get_total_price(self, cart: Cart):
        return sum(
            [item.product_stock.price * item.quantity for item in cart.items.all()]
        )


class OrderItemSerializer(serializers.ModelSerializer):
    product_stock = SimpleProductSerializer(source="product_stock.product")
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["id", "product_stock", "quantity", "total_price"]

    def get_total_price(self, order_item: OrderItem):
        return order_item.product_stock.price * order_item.quantity


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "user", "status", "total_price", "created_at", "items"]


class OrderCreateSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError(
                "Cart does not exist or does not belong to the user."
            )
        if not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError("Cart is empty.")

        return cart_id

    def create(self, validated_data):
        user_id = self.context.get("user_id")
        cart_id = validated_data["cart_id"]
        try:
            order = OrderService.create_order(user_id=user_id, cart_id=cart_id)
            return order
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def to_representation(self, instance):
        return OrderSerializer(instance).data


class WishlistProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name"]


class WishlistSerializer(serializers.ModelSerializer):
    products = WishlistProductSerializer(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = ["id", "user", "products", "created_at"]
        read_only_fields = ["user"]
