from django.contrib import admin


from . import models


class ImageAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "id",
        "get_categories_str",
        "get_linked_image_tag"
    ]

    list_filter = [
        "categories"
    ]

    readonly_fields = [
        "get_linked_image_tag"
    ]

    fields = [
        "title",
        "categories",
        "image",
        "get_linked_image_tag"
    ]


# ProductAdmin
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "price",
        "get_sizes_str",
        "get_categories_str",
        "get_linked_image_tag"
    ]

    list_filter = [
        "categories"
    ]

    readonly_fields = [
        "get_linked_image_tag"
    ]

    fields = [
        "title",
        "description",
        "categories",
        "sizes",
        "image",
        "get_linked_image_tag",
        "price"

    ]



# OrderedProduct
class OrderedProductAdmin(admin.ModelAdmin):
    list_display = [
        "order",
        "id",
        "get_linked_image_tag",
        "product",
        "size",
        "amount"
    ]

    list_filter = [
        "order",
        "product",
    ]




admin.site.register(models.Adress)
admin.site.register(models.Category)
admin.site.register(models.Image, ImageAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Order)
admin.site.register(models.OrderedProduct, OrderedProductAdmin)
admin.site.register(models.Size)
