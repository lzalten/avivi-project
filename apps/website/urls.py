from django.contrib import admin
from django.urls import path, include
from . import views
from .views import *
from ..payments.stripe.views import CreateCheckoutSessionView, SuccessView, CancelView

urlpatterns = [
    path("chat/", Rooms.as_view(), name="rooms"),
    path("chat/<str:slug>", Room.as_view(), name="room"),
    path("chat/create/", CreateChat.as_view(), name="create"),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('products/', ProductList.as_view(), name='product_list'),
    path('create_order/<int:product_id>/', CreateOrder.as_view(), name='create_order'),
    path('orders/', OrderList.as_view(), name='order_list'),
    path('add_product/', AddProduct.as_view(), name='add_product'),
    path('edit_product/<int:product_id>/', EditProduct.as_view(), name='edit_product'),
    path('user_products/', UserProducts.as_view(), name='user_products'),
    path('create_checkout_session/<int:order_id>/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('success_payment/', SuccessView.as_view(), name='success_payment'),
    path('decline_payment/', CancelView.as_view(), name='decline_payment'),
]
