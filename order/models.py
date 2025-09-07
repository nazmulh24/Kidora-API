from django.db import models
from django.core.validators import MinValueValidator
from uuid import uuid4

from users.models import User
from product.models import Product


class Wishlist(models.Model):
    """User's persistent wishlist of products (one per user)."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wishlist")
    products = models.ManyToManyField(Product, related_name="wishlisted_by", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist of {self.user.email}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"


class Cart(models.Model):
    """User's shopping cart."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.email}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Cart"
        verbose_name_plural = "Carts"


class CartItem(models.Model):
    """Item in a cart."""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product_stock = models.ForeignKey("product.ProductStock", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [["cart", "product_stock"]]
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"

    def __str__(self):
        return f"{self.quantity} x {self.product_stock.product.name} ({self.product_stock.size})"


class Order(models.Model):
    """User's order."""

    NOT_PAID = "Not Paid"
    READY_TO_SHIP = "Ready to Ship"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELED = "Canceled"

    STATUS_CHOICES = [
        (NOT_PAID, "Not Paid"),
        (READY_TO_SHIP, "Ready to Ship"),
        (SHIPPED, "Shipped"),
        (DELIVERED, "Delivered"),
        (CANCELED, "Canceled"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=NOT_PAID)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.first_name}_{self.user.last_name}({self.user.email}) - Status: {self.status}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderItem(models.Model):
    """Item in an order."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_stock = models.ForeignKey("product.ProductStock", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product_stock.product.name} ({self.product_stock.size})"
        return f"{self.quantity} x {self.product.name}"

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
