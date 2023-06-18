"""
URL configuration for web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from products import views
from .views import Catalog

urlpatterns = [
    # path('', views.mainpage, name='mainpage')
    # path('product/?P<product_id>\w+)/$', views.product, name='product'),
    path('product/<int:product_id>/', views.product, name='product'),
    path('catalog', Catalog.as_view(), name='catalog'),
    path('filter/', views.FilterCatalogView.as_view(), name='filter'),
    # path('catalog/category/<int:category_id>/', views.category, name='category'),
]
