from django.urls import path, include
from rest_framework_nested import routers

from product.views import CategoryViewSet

router = routers.DefaultRouter()
router.register("categories", CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
    #
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    #
]
