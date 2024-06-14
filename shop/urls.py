from django.urls import path

from . import views

urlpatterns = [
    path("", views.product_list, name="shop-index"),
    path("product/detail/<int:id>", views.product_detail, name="shop-product-detail"),
    path("shopping-cart", views.shopping_cart, name="shop-shopping-cart"),
    path("delete-cart-item/<int:id>", views.delete_ordered_product, name="shop-delete-item"),
    path("add-item", views.add_item, name="shop-add-item"),
    path("add-item-to-cart", views.add_item_to_cart, name="shop-add-item-to-cart"),

]