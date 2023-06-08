from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns=[
     # ------------------------------------------- Auth --------------------------------------------------------- #
    
    path('login', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
]