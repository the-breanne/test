from django.conf.urls import url, include
from . import views
from django.urls import path, re_path
from django.contrib.auth import views as auth_views


app_name = 'crm1'
urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^home/$', views.home, name='home'),
    path('customer_list', views.customer_list, name='customer_list'),
    path('customer/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('customer/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('customer/<int:pk>/summary/', views.summary, name='summary'),
    path('prod', views.prod, name='prod'),
    path('product/create/', views.product_new, name='product_new'),
    path('product/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    #path('login/', auth_views.LoginView.as_view(template_name='crm1/login.html'), name='login'),
    path('contact', views.contact, name='contact'),
    path('accounts/', include('django.contrib.auth.urls')),

# reset password

    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset_password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetConfirmView.as_view(), name="reset_password_complete"),



]
