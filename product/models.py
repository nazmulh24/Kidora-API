from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

from product.validators import validate_file_size


class Category(models.Model):
    """Product category."""

    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(models.Model):
    """Product in the store."""

    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"

    STATUS_CHOICES = [
        (XS, "XS"),
        (S, "S"),
        (M, "M"),
        (L, "L"),
        (XL, "XL"),
        (XXL, "XXL"),
    ]

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    size = models.CharField(max_length=5, choices=STATUS_CHOICES, default=M)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def is_in_stock(self):
        """Return True if the product is in stock."""
        return self.stock > 0

    def total_reviews(self):
        """Return the total number of reviews for this product."""
        return self.review_set.count()

    def average_rating(self):
        """Return the average rating for this product, rounded to 1 decimal or 0 if no reviews."""
        avg = self.review_set.aggregate(avg_rating=Avg("rating"))["avg_rating"]
        if avg is None:
            return 0
        return float(f"{avg:.1f}")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(
        upload_to="products/images",
        validators=[validate_file_size],
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Image for {self.product.name}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],
    )
    comment = models.TextField()
    image = models.ImageField(upload_to="reviews/images", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review of {self.product.name} by {self.user.first_name} {self.user.last_name}"
