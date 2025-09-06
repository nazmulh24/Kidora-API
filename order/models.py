from django.db import models
from users.models import User
from product.models import Product


class Wishlist(models.Model):
    """User's wishlist of products."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wishlist")
    products = models.ManyToManyField(Product, related_name="wishlisted_by")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist of {self.user.username}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"


class Cart(models.Model):
    """User's shopping cart."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.email}"

    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Cart"
        verbose_name_plural = "Carts"


class CartItem(models.Model):
    """Item in a cart."""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def line_total(self):
        return self.quantity * self.product.price

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"


class Order(models.Model):
    """User's order."""

    PENDING = "Pending"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (SHIPPED, "Shipped"),
        (DELIVERED, "Delivered"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=PENDING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.email}"

    def item_count(self):
        return sum(item.quantity for item in self.items.all())

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderItem(models.Model):
    """Item in an order."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def line_total(self):
        return self.quantity * self.price

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
