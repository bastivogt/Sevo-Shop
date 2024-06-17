from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.contrib import messages


from . import models
from . import forms

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


    try:
        order = models.Order.objects.get(user=user, done=False)
    except:
        order = models.Order(user=user)
        order.order_id = order.create_order_id()
        order.save()

    orderedProduct = models.OrderedProduct(product=product, order=order)
    form = forms.OrderedProductFEForm(instance=orderedProduct)

    

    return render(request, "shop/product_detail.html", {
        "title": "PRODUCT DETAIL",
        "product": product,

        "form": form
    })















@login_required(login_url="sevo-auth-login")
def add_item_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product-id")
        product_size = request.POST.get("product-size")
        product_amount = request.POST.get("product-amount")

        print(f"product_id: {product_id}")
        print(f"product_size: {product_size}")
        print(f"product_amount: {product_amount}")

        if product_id != None and product_size != None and product_amount != None:
            try:
                order = models.Order.objects.get(user=request.user, done=False)
            except:
                order = models.Order(user=request.user)
                order.order_id = order.create_order_id()
                order.save()
                #messages.add_message(request, messages.SUCCESS, _("Added product to cart."))
            
        product = get_object_or_404(models.Product, id=int(product_id))
        size = get_object_or_404(models.Size, id=int(product_size))

        

        try:
            orderedProduct = models.OrderedProduct.objects.get(order=order, size=size, product=product)
            orderedProduct.amount += int(product_amount)
        except:
            orderedProduct = models.OrderedProduct(order=order, size=size, product=product, amount=int(product_amount))
        orderedProduct.save()

  
        messages.add_message(request, messages.SUCCESS, _("Product added to cart!"))
        return JsonResponse({"status": "success"})
    else:
        messages.add_message(request, messages.ERROR, _("Something went wrong"))
        return JsonResponse({"status": "fail"})

    #return HttpResponse("ADD ITEM TO CART")
    



@login_required(login_url="sevo-auth-login")
def add_item(request):
    
    if request.method == "POST":
        user = request.user

        product_id = int(request.POST.get("product"))
        print(int(product_id))
        
        product = get_object_or_404(models.Product, id=product_id)

        try:
            order = models.Order.objects.get(user=user, done=False)
        except:
            order = models.Order(user=user)
            order.order_id = order.create_order_id()
            order.save()

        orderedProduct = models.OrderedProduct(product=product, order=order)
        form = forms.OrderedProductFEForm(request.POST, instance=orderedProduct)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _("Product added to cart!"))
            return JsonResponse({"status": "success"})
        else:
            print(form.errors)
            messages.add_message(request, messages.ERROR, form.errors)
            return JsonResponse({"status": "fail"})









def update_ordered_product(request, order):
    item_id = request.POST.get("item-id")
    item_amount = request.POST.get("item-amount")
    print(item_id)
    print(order)
    if int(item_amount) < 1:
        item_amount = "1"

    try:
        ordered_product = models.OrderedProduct.objects.get(order=order, id=int(item_id))
        ordered_product.amount = int(item_amount)
        ordered_product.save()
        messages.add_message(request, messages.SUCCESS, _("Update success!"))
    except:
        messages.add_message(request, messages.ERROR, _("Update fail!"))

        

@login_required(login_url="sevo-auth-login")
def delete_ordered_product(request, id):
    item = get_object_or_404(models.OrderedProduct, id=id)
    item.delete()
    messages.add_message(request, messages.SUCCESS, _("Product deleted!"))
    url = reverse("shop-shopping-cart")
    return HttpResponseRedirect(url)


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

    if request.method == "POST":
        print("ORDER")
        print(order)
        update_ordered_product(request, order=order)
    else:
        pass
    return render(request, "shop/shopping_cart.html", {
        "title": _("Shopping Cart"),
        "order": order
    })