from django.db import models
from django.contrib import admin
from django.utils.html import format_html
from tinymce import models as tinymce_models

from django.core.validators import MinValueValidator, MaxValueValidator



from django.contrib.auth import get_user_model
User = get_user_model()


from shop.helpers import create_token

# Create your models here.







# Adress
class Adress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=25)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.street} {self.house_number}, {self.postal_code} {self.city}, {self.country}"

    class Meta:
        verbose_name_plural = "Adresses"


# Category
class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Categories"
    

# Sizes
class Size(models.Model):
    title = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Image
class Image(models.Model):
    title = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category, blank=True)
    image = models.ImageField(upload_to="shop/images")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @admin.display(description="Image")
    def get_image_tag(self):
        img_tag = f'<img src="{self.image.url}" style="width: 80px; height: 80px; object-fit: cover;" title="{self.title}" alt="{self.title}" />'
        return format_html(img_tag)
    
    @admin.display(description="Linked Image")
    def get_linked_image_tag(self):
        a_tag = f'<a href="{self.image.url}" title="{self.title}">{self.get_image_tag()}</a>'
        return format_html(a_tag)
    
    @admin.display(description="Categories")
    def get_categories_str(self):
        cats = self.categories.all().order_by("title")
        cats_list = [cat.title for cat in cats]
        return ", ".join(cats_list)
    
    @admin.display(description="URL")
    def get_url(self):
        if self.image:
            return self.image.url
        return None

    def delete(self, *args, **kwargs):
        self.image.delete()
        return super().delete(*args, **kwargs)
    
    def __str__(self):
        return f"#{self.id} - {self.title}"
    

# Product
class Product(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = tinymce_models.HTMLField()
    categories = models.ManyToManyField(Category, blank=True)
    sizes = models.ManyToManyField(Size, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL)



    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    @admin.display(description="Categories")
    def get_categories_str(self):
        cats = self.categories.all().order_by("title")
        cats_list = [cat.title for cat in cats]
        return ", ".join(cats_list)
    

    @admin.display(description="Sizes")
    def get_sizes_str(self):
        sizes = self.sizes.all()
        sizes_list =[size.title for size in sizes]
        return ", ".join(sizes_list)
    
    @admin.display(description="Linked Image")
    def get_linked_image_tag(self):
        return self.image.get_linked_image_tag()

    @admin.display(description="Image")
    def get_image_tag(self):
        return self.image.get_image_tag()

    def __str__(self):
        return self.title
    

# Order
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=27)
    done = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def create_order_id(self):
        return create_token()
    
 
    def get_total_price(self):
        all_products = self.orderedproduct_set.all()
        total_price = 0
        for ordered_product in all_products:
            total_price += ordered_product.get_total_price()
        return total_price
    
 
    def get_products_count(self):
        all_products = self.orderedproduct_set.all()
        amount = 0
        for item in all_products:
            amount += item.amount
        return amount
    
    def get_products(self):
        return self.orderedproduct_set.all()
    
    def __str__(self):
        return self.order_id
    

# OrderdProduct
class OrderedProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, null=True, on_delete=models.SET_NULL)
    amount = models.IntegerField(default=1, validators=[
        MinValueValidator(1)
    ])
    

    @admin.display(description="Linked Image")
    def get_linked_image_tag(self):
        return self.product.get_linked_image_tag() 



    def get_price(self):
        return self.product.price
    

    def get_total_price(self):
        return self.amount * self.product.price

    def __str__(self):
        return f"{self.order.order_id} - {self.product.title}"

        


