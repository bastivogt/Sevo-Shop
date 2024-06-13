from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.contrib import messages


from . import models

# Create your views here.


@login_required(login_url="sevo-auth-login")
def redirect_view(request):
    url = reverse("shop-index")
    return HttpResponseRedirect(url)



@login_required(login_url="sevo-auth-login")
def product_list(request):
    products = models.Product.objects.all()

    return render(request, "shop/product_list.html", {
        "title": _("All Products"),
        "products": products
    })


@login_required(login_url="sevo-auth-login")
def product_detail(request, id):
    user = request.user
    product = get_object_or_404(models.Product, id=id)
    product_sizes = product.sizes.all()

    if request.method == "POST":
        update_shopping_cart(request)
    else:
        pass
    return render(request, "shop/product_detail.html", {
        "title": "PRODUCT DETAIL",
        "product": product,
        "product_sizes": product_sizes
    })



def update_shopping_cart(request):

    product_id = request.POST.get("product-id")
    product_size = request.POST.get("product-size")
    product_amount = request.POST.get("product-amount")

    if product_id != None and product_size != None and product_amount != None:
        try:
            order = models.Order.objects.get(user=request.user, done=False)
        except:
            order = models.Order(user=request.user)
            order.order_id = order.create_order_id()
            order.save()
        
        product = get_object_or_404(models.Product, id=int(product_id))
        size = get_object_or_404(models.Size, id=int(product_size))

        try:
            orderedProduct = models.OrderedProduct.objects.get(order=order, size=size, product=product)
            orderedProduct.amount += int(product_amount)
        except:
            orderedProduct = models.OrderedProduct(order=order, size=size, product=product, amount=int(product_amount))
        orderedProduct.save()

        msg = f"{product.title} added to Cart!"
        messages.add_message(request, messages.SUCCESS, _(msg))
    else:
        msg = f"Something went wrong!"
        messages.add_message(request, messages.SUCCESS, _(msg))


        





@login_required(login_url="sevo-auth-login")
def shopping_cart(request):
    print("CART")
    try:
        order = models.Order.objects.get(user=request.user, done=False)
        print(order.orderedproduct_set.all())
        print(order.get_products())
        print(order.get_products_count())
        print(order.get_total_price())
    except:
        order = None
    return render(request, "shop/shopping_cart.html", {
        "title": _("Shopping Cart"),
        "order": order
    })