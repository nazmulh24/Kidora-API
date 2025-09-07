from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

from product.validators import validate_file_size
from cloudinary.models import CloudinaryField


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

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    video_url = models.URLField(
        blank=True,
        null=True,
        help_text="Paste a YouTube video URL here. Example: https://www.youtube.com/watch?v=xxxxxx",
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def is_in_stock(self):
        """Return True if any size is in stock."""
        return self.stocks.filter(stock__gt=0).exists()

    @property
    def total_stock(self):
        return self.stocks.aggregate(total=models.Sum("stock"))["total"] or 0


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


class ProductStock(models.Model):
    SIZE_CHOICES = [
        ("XS", "XS"),
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
        ("XXL", "XXL"),
    ]
    product = models.ForeignKey(
        Product, related_name="stocks", on_delete=models.CASCADE
    )
    size = models.CharField(max_length=5, choices=SIZE_CHOICES)
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.size}: {self.stock} pcs"

    class Meta:
        unique_together = ("product", "size")
        verbose_name = "Product Stock"
        verbose_name_plural = "Product Stocks"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = CloudinaryField(
        "image",
        blank=True,
        null=True,
        validators=[validate_file_size],
        folder="Kidora/products/images",
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review of {self.product.name} by {self.user.first_name} {self.user.last_name}"


class ReviewImage(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = CloudinaryField(
        "image",
        blank=True,
        null=True,
        validators=[validate_file_size],
        folder="Kidora/reviews/images",
    )

    def __str__(self):
        return f"Image for review {self.review.id}"
