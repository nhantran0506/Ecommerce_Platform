from django.urls import path, include

urlpatterns = [
    path('shops/', include('apps.Shops.urls')),
    path('users/', include('apps.Users.urls')),
    path('products/', include('apps.Products.urls')),
    path('categories/', include('apps.Categories.urls')),
    path('carts/', include('apps.Carts.urls')),
    path('orders/', include('apps.Orders.urls')),
    path('admin/', include('apps.Admin.urls')),
    path('chatbot/', include('apps.ChatBot.urls')),
    path('recommendations/', include('apps.Recommendation.urls')),
    path('embedding/', include('apps.Embedding.urls')),
    path('notifications/', include('apps.Notify.urls')),
] 