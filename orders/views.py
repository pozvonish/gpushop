from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .forms import CheckoutContactForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
# def mainpage(request):
#     form = UsersForm(request.POST or None)
#     return render(request, 'mainpage/mainpage.html', locals())

def basket_adding(request):
    return_dict = dict()
    if request.user.is_authenticated:
        session_key = request.user.id
    else:
        session_key = request.session.session_key
    data=request.POST
    product_id = data.get('product_id')
    count = data.get('count')
    is_delete=data.get('is_delete')

    if is_delete == 'true':
        # ProductInBasket.objects.filter(id=product_id).update(is_active=False) #deactivate
        ProductInBasket.objects.filter(id=product_id).delete() #clear
    else:
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id, is_active=True, defaults={'count': count})
        if not created:
            new_product.count += int(count)
            new_product.save(force_update=True)

    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    products_total_count = products_in_basket.count()
    return_dict['products_total_count'] = products_total_count

    return_dict['products'] = list()

    for item in products_in_basket:
        product_dict = dict()
        product_dict['id'] = item.id
        product_dict['name'] = item.product.name
        product_dict['price_per_item'] = item.price_per_item
        product_dict['count'] = item.count
        return_dict['products'].append(product_dict)

    return JsonResponse(return_dict)

def basket_editing(request):
    return_dict = dict()
    if request.user.is_authenticated:
        session_key = request.user.id
    else:
        session_key = request.session.session_key
    data = request.POST
    # print(data)
    product_id = data.get('id')
    count = data.get('count')
    if int(count) > 0:
        product = ProductInBasket.objects.get(session_key=session_key, id=product_id, is_active=True)
        product.count = int(count)
        product.save(force_update=True)

    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    products_total_count = products_in_basket.count()
    return_dict['products_total_count'] = products_total_count

    return_dict['products'] = list()

    for item in products_in_basket:
        product_dict = dict()
        product_dict['id'] = item.id
        product_dict['name'] = item.product.name
        product_dict['price_per_item'] = item.price_per_item
        product_dict['count'] = item.count
        return_dict['products'].append(product_dict)

    # print(return_dict)
    return JsonResponse(return_dict)

def basket(request):
    if request.user.is_authenticated:
        session_key = request.user.id
    else:
        session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True).exclude(order__isnull=False)
    return render(request, 'basket/basket.html', locals())


def checkout(request):
    if request.user.is_authenticated:
        session_key = request.user.id
        products_in_basket = ProductInBasket.objects.filter(session_key = session_key, is_active = True).exclude(order__isnull = False)
        form = CheckoutContactForm(request.POST or None)
        order_sent = False
        if request.POST:
            if form.is_valid():
                print('OK')
                data = request.POST
                comment = data.get("comment", None)
                adress = data["adress"]
                # user, created = User.objects.get_or_create(username = phone, defaults={'first_name': name})

                order = Order.objects.create(user = request.user, customer_name = request.user.last_name + ' ' + request.user.first_name,
                                             customer_adress = adress, comment = comment, customer_email = request.user.email, status_id = 1)
                for name, value in data.items():
                    if name.startswith("product_in_basket_"):
                        product_in_basket_id = name.split('product_in_basket_')[1]

                        product_in_basket = ProductInBasket.objects.get(id = product_in_basket_id)
                        product_in_basket.order = order
                        product_in_basket.save(force_update=True)

                        ProductInOrder.objects.create(product = product_in_basket.product, count = product_in_basket.count,
                                                      price_per_item = product_in_basket.price_per_item,
                                                      total_price = product_in_basket.total_price,
                                                      order = order)
                        product_in_basket.delete()

                order_sent = True
            else:
                print('ERROR')

        context = {'order_sent': order_sent}

        return render(request, 'checkout/checkout.html', locals())

    else:
        return redirect('login')


def success(request):
    return render(request, 'checkout/success.html', locals())