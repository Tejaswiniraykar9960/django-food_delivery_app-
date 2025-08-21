"""
URL configuration for food_delivery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from food import views 

urlpatterns = [
    path("admin/", admin.site.urls),
        path('', views.home, name='home'),
    path('restaurant/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),

    # Auth & registration
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),  # login/logout/password reset

    # Restaurant management
    path('create-restaurant/', views.create_restaurant_profile, name='create_restaurant'),
    path('restaurant/dashboard/', views.restaurant_dashboard, name='restaurant_dashboard'),
    path('restaurant/menu/create/', views.menu_item_create, name='menu_item_create'),
    path('restaurant/menu/<int:pk>/edit/', views.menu_item_edit, name='menu_item_edit'),

    # Cart
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),

    # Orders
    path('orders/', views.my_orders, name='my_orders'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),

    # API endpoint
    path('api/menu/<int:restaurant_id>/', views.api_menu_items, name='api_menu_items'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


