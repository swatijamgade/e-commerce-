from django.contrib import admin
from django.urls import path

from .views import product_list, product_detail, load_products

app_name = "products"

urlpatterns = [

    path('', product_list, name="product_list"),
    # path('page/', test_session, name="count"),
    path('load/', load_products, name="load"),
    path('<slug:category_slug>/', product_list, name="product_list_by_category"),
    path('<int:product_id>/<slug:slug>/', product_detail, name="product_detail"),

]