from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('<uuid:product_id>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('<uuid:product_id>/ratings/', views.ProductRatingsView.as_view(), name='product-ratings'),
    path('<uuid:product_id>/images/', views.ProductImagesView.as_view(), name='product-images'),
]