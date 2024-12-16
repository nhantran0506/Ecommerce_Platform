from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='category-list'),
    path('<uuid:cat_id>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('<uuid:cat_id>/products/', views.CategoryProductsView.as_view(), name='category-products'),
]