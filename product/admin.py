from django.contrib import admin
from product.models import Product, ProductImage, Category, Review, ReviewImage

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(ReviewImage)
