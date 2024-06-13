from django.urls import path

from . import views

urlpatterns = [
    path("", views.product_list, name="shop-index"),
    path("shop/product/detail/<int:id>", views.product_detail, name="shop-product-detail"),
    path("shopping-cart", views.shopping_cart, name="shop-shopping-cart"),

]