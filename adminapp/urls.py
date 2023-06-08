from adminapp import views
from django.urls import path

urlpatterns = [
    path('',views.admin_index,name='admin_index'),
    
    # --------------------------- Category ---------------------------------------------- #
    
    path('category/', views.category_list, name='category_list'),
    path('category/add/', views.category_add, name='category_add'),
    path('categories/edit/<int:category_id>/', views.category_edit, name='category_edit'),
    path('categories/delete/<int:category_id>/', views.category_delete, name='category_delete'),
    
    #----# 
    
    path('categories/<int:category_id>/products/', views.category_products, name='category_products'),
    
    # ------------------------------ Product ----------------------------- #
    
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('product_list/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/delete/<int:product_id>/', views.product_delete, name='product_delete'),
    
    path('<int:product_id>/edit_image', views.edit_product_image, name='edit_product_image'),
    
    # ---------------------- For product avalability toggle on/of switch --------------------#
        
    path('toggle_availability/<int:product_id>/', views.toggle_availability, name='toggle_availability'),
    
    
]