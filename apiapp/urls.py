from django.urls import path
from apiapp import views

urlpatterns = [
    path('categories/', views.category_list_api),
    path('categories/<int:pk>/', views.category_detail_api),
    
    path('categories/<int:category_id>/products/', views.CategoryProductsAPIView.as_view(), name='category-products-api'),
     
    path('products/', views.product_list_api, name='product-list'),
    path('product/<int:pk>/', views.product_detail_api, name='product-detail'),
    
    path('products/<int:product_id>/', views.ProductDetailAPI.as_view(), name='product_detail_api'),
    
    path('product-prices/', views.product_price_list_api, name='product-price-list'),
    path('product-prices/<int:pk>/', views.product_price_detail_api, name='product-price-detail'),
    
    path('user/', views.user_list_api,),
    
    path('carts/', views.cart_list_api, name='cart-list'),
    path('my-carts', views.my_carts_api,),
    path('cart-items/', views.cart_items_view, name='cart_items'),
    path('carts/<int:pk>/', views.cart_detail_api, name='cart-detail'),
    
    
    path('order-items/', views.order_item_list_api, name='order_item_list'),
    path('order-items/<int:pk>/', views.order_item_detail_api, name='order_item_detail'),
    
    path('orders/', views.order_list_api, name='order_list'),
    path('orders/<int:pk>/', views.order_detail_api, name='order_detail'),

]



