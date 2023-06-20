from django.urls import path
from apiapp import views

urlpatterns = [
    path('categories/', views.category_list_api),
    path('categories/<int:pk>/', views.category_detail_api),
    
    path('products/', views.product_list_api, name='product-list'),
    path('product/<int:pk>/', views.product_detail_api, name='product-detail'),
    
    path('product-prices/', views.product_price_list_api, name='product-price-list'),
    path('product-prices/<int:pk>/', views.product_price_detail_api, name='product-price-detail'),
    
    path('order-items/', views.order_item_list_api, name='order_item_list'),
    path('order-items/<int:pk>/', views.order_item_detail_api, name='order_item_detail'),
    
    path('orders/', views.order_list_api, name='order_list'),
    path('orders/<int:pk>/', views.order_detail_api, name='order_detail'),

]



