import random
from itertools import chain
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import View

from .helpers.ChatHelper import ChatHelper
from .models import Product, Order, Message, Room as ModelRoom
from django.contrib.auth.models import User, Group


class RegisterView(View):
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
        return render(request, 'register.html', {'form': form})

    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('product_list')
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')


class LogoutView(LoginRequiredMixin,View):
    def get(self, request):
        logout(request)
        return redirect('login')


class ProductList(LoginRequiredMixin, View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'product_list.html', {'products': products})


class CreateOrder(LoginRequiredMixin, View):

    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        return render(request, 'create_order.html', {'product': product})

    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        count = int(request.POST.get('count', 1))
        Order.objects.create(user=request.user, item=product, count=count, total_price=product.price * count,
                             paid=False)
        return redirect('order_list')


class OrderList(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user, paid=0)
        return render(request, 'order_list.html', {'orders': orders})


class AddProduct(LoginRequiredMixin, View):
    def post(self, request):
        try:
            name = request.POST.get('name')
            price = int(request.POST.get('price'))
            description = request.POST.get('description')
        except Exception as e:
            return render(request, 'add_product.html')

        if type(name) is str and type(price) is int and type(description) is str:
            Product.objects.create(
                user=request.user,
                name=name,
                price=price,
                description=description
            )
            return redirect('product_list')
        return render(request, 'add_product.html')

    def get(self, request):
        return render(request, 'add_product.html')


class EditProduct(LoginRequiredMixin, View):

    def post(self, request, product_id):
        try:
            product = get_object_or_404(Product, pk=product_id, user=request.user)
            product.name = request.POST.get('name')
            product.price = int(request.POST.get('price'))
            product.description = request.POST.get('description')
            product.save()
        except Exception as e:
            return render(request, 'edit_product.html', {'product': product})
        return redirect('user_products')

    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id, user=request.user)
        return render(request, 'edit_product.html', {'product': product})


class UserProducts(LoginRequiredMixin, View):
    def get(self, request):
        products = Product.objects.filter(user=request.user)
        return render(request, 'user_products.html', {'products': products})


class Rooms(LoginRequiredMixin, View):
    def get(self, request):
        rooms = list(chain(ModelRoom.objects.filter(client=request.user), ModelRoom.objects.filter(manager=request.user)))
        return render(request, "rooms.html", {"rooms": rooms})


class Room(LoginRequiredMixin, View):
    def get(self, request, slug):
        try:
            room = ModelRoom.objects.get(slug=slug)
            messages = Message.objects.filter(room=room)
        except Exception as e:
            print(e)
            redirect('product_list')
        return render(request, "room.html", {"room": room, "slug": slug, 'messages': messages})


class CreateChat(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.groups.filter(name='manager').exists() or request.user.is_superuser:
            return redirect('product_list')
        else:
            ChatHelper().create_room(request.user)
            return redirect('rooms')


