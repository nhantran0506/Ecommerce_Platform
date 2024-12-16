from django.urls import path
from . import views

app_name = 'carts'

urlpatterns = [
    path('', views.CartView.as_view(), name='cart-detail'),
    path('products/', views.CartProductsView.as_view(), name='cart-products'),
]