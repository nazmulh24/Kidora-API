from django.contrib import admin
from product.models import (
    Product,
    ProductImage,
    ProductStock,
    Category,
    Review,
    ReviewImage,
)

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductStock)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(ReviewImage)
