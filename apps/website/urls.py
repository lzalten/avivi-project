from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.rooms, name="rooms"),
    path("<str:slug>", views.room, name="room"),
    path("create/", views.create_chat, name="create"),
]