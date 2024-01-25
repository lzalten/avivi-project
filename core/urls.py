"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from apps.api import urls as apiurls
from apps.website.views import *
from apps.payments.stripe.views import CreateCheckoutSessionView, SuccessView, CancelView

urlpatterns = [
    path('', login_view),
    path('chat/',include('apps.website.urls')),
    path('api/', include(apiurls)),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin/', admin.site.urls, name='admin'),
    path('products/', product_list, name='product_list'),
    path('create_order/<int:product_id>/', create_order, name='create_order'),
    path('orders/', order_list, name='order_list'),
    path('add_product/', add_product, name='add_product'),
    path('edit_product/<int:product_id>/', edit_product, name='edit_product'),
    path('user_products/', user_products, name='user_products'),
    path('create_checkout_session/<int:order_id>/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('success_payment/', SuccessView.as_view()),
    path('decline_payment/', CancelView.as_view()),
]
