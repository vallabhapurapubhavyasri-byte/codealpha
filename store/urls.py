from django.urls import path
from . import views

urlpatterns = [
    # Navigation pages
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('product/preview/', views.product_detail_preview, name='product_detail_preview'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    
    # User Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Cart & Checkout Actions
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/process/', views.process_order, name='process_order'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
]
