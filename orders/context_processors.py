from .models import ProductInBasket

def getting_basket_info(request):
    if request.user.is_authenticated:
        session_key = request.user.id
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()

    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    products_total_count = products_in_basket.count()


    return locals()