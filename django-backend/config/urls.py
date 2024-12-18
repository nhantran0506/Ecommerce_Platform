"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view 


schema_view = get_schema_view(
    openapi.Info(
        title="Ecommerce App APIs",
        default_version = "3.0.0"
    ),
    public=True, # role restrict 
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("docs/", include([
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
        path('swagger/schema/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema')
    ]))
]
