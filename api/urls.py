from django.urls import path, include
from rest_framework_nested import routers

from product.views import (
    CategoryViewSet,
    ProductViewSet,
    ProductImageViewSet,
    ProductStockViewSet,
    ReviewViewSet,
    ReviewImageViewSet,
)
from order.views import CartViewSet, CartItemViewSet, OrderViewSet, WishlistViewSet

router = routers.DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("products", ProductViewSet, basename="products")
router.register("carts", CartViewSet, basename="carts")
router.register("orders", OrderViewSet, basename="orders")
router.register("wishlists", WishlistViewSet, basename="wishlists")

product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
product_router.register("reviews", ReviewViewSet, basename="product-review")
product_router.register("images", ProductImageViewSet, basename="product-images")
product_router.register("stocks", ProductStockViewSet, basename="product-stocks")

review_router = routers.NestedDefaultRouter(product_router, "reviews", lookup="review")
review_router.register("images", ReviewImageViewSet, basename="review-images")

cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cart_router.register("items", CartItemViewSet, basename="cart-item")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(product_router.urls)),
    path("", include(review_router.urls)),
    path("", include(cart_router.urls)),
    #
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    #
]
