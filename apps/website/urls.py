from django.contrib import admin
from django.urls import path, include
from . import views
from .views import *
from ..payments.stripe.views import CreateCheckoutSessionView, SuccessView, CancelView

urlpatterns = [
    path("chat/", views.rooms, name="rooms"),
    path("chat/<str:slug>", views.room, name="room"),
    path("chat/create/", views.create_chat, name="create"),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
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