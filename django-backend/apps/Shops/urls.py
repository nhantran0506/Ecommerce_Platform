from django.urls import path
from . import views

app_name = 'shops'

urlpatterns = [
    path('', views.ShopListView.as_view(), name='shop-list'),
    path('<uuid:shop_id>/', views.ShopDetailView.as_view(), name='shop-detail'),
    path('<uuid:shop_id>/products/', views.ShopProductsView.as_view(), name='shop-products'),
    path('<uuid:shop_id>/ratings/', views.ShopRatingsView.as_view(), name='shop-ratings'),
]