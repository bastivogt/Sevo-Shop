from shop import models

def order_context(request):
    order = None
    if request.user.is_authenticated:
        try:
            order = models.Order.objects.get(user=request.user, done=False)
            # print(order.orderedproduct_set.all())
            # print(order.get_products())
            # print(order.get_products_count())
            # print(order.get_total_price())
        except:
            order = None
    return {
        "proc_order": order
    }