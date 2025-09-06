from django.urls import path, include
from rest_framework_nested import routers

from product.views import CategoryViewSet, ProductViewSet

router = routers.DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("products", ProductViewSet, basename="products")

urlpatterns = [
    path("", include(router.urls)),
    #
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    #
]
