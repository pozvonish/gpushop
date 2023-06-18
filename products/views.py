from django.shortcuts import render
from products.models import *
from orders.models import *

from django.views.generic import ListView
from django.views.generic.base import View
#
#
# def mainpage(request):
#     form = UsersForm(request.POST or None)
#     return render(request, 'mainpage/mainpage.html', locals())

class Category:
    def get_cats(self):
        return reversed(ProductCategory.objects.all())

def product(request, product_id):
    if request.user.is_authenticated:
        session_key = request.user.id
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()

    product=Product.objects.get(id=product_id)
    product_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, product__is_active=True, product_id=product_id)

    return render(request, 'products/product.html', locals())

def catalog(request):
    product_categories = reversed(ProductCategory.objects.filter())
    products_images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True).order_by('product__price')
    return render(request, 'catalog/catalog.html', locals())

def category(request, category_id):
    product_categories = reversed(ProductCategory.objects.filter())
    products_images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True, product__category=category_id).order_by('product__price')
    return render(request, 'catalog/catalog.html', locals())

class Catalog(Category, ListView):
    model = ProductImage
    template_name = 'catalog/catalog.html'
    context_object_name = 'products_images'

    def get_queryset(self):
        return ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True)

class FilterCatalogView(Category, ListView):
    template_name = 'catalog/catalog.html'
    context_object_name = 'products_images'
    def get_queryset(self):
        cat_id = self.request.GET.get('category')
        sort = self.request.GET.get('sort')
        if cat_id == 'all':
            queryset = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True).order_by(sort)
        else:
            queryset = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True, product__category_id=cat_id).order_by(sort)
        return queryset