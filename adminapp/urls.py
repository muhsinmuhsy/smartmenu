from adminapp import views
from django.urls import path

urlpatterns = [
    path('',views.admin_index,name='admin_index'),
    
    path('order/<int:order_id>/', views.order_details, name='order_details'),
    path('type/<int:order_id>/', views.type_details, name='type_details'),
    
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
    
    
    # --------------------------------- Report ----------------------------------------- #
    
    path('report/', views.report, name='report'),
    path('report/<int:order_id>/', views.report_detalis, name='report_detalis'),
     # --------------------------------- Table ----------------------------------------- #
     
    path('tables/', views.table_list, name='table_list'),
    path('tables/create/', views.table_create, name='table_create'),
    path('tables/<int:table_id>/update/', views.table_update, name='table_update'),
    path('tables/<int:table_id>/delete/', views.table_delete, name='table_delete'),
    
    
    # path('tables/status/', views.table_status, name='table_status'),
    # path('tables/filter/', views.table_filter, name='table_filter'),
    # path('tables/sort/', views.table_sort, name='table_sort'),
    # path('tables/<int:table_id>/assign/<int:order_id>/', views.table_assign, name='table_assign'),
    
    # ---------------------- For product avalability toggle on/of switch --------------------#
        
    path('toggle_availability/<int:product_id>/', views.toggle_availability, name='toggle_availability'),
    path('toggle_category_availability/<int:category_id>/', views.toggle_category_availability, name='toggle_category_availability'),
    
    
    
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
 

    
    # --------------------------------------------------------------- #
    
    path('table_main/<int:table_id>/', views.table_main, name='table_main')
    
]


