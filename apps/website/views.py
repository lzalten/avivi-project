import random
from itertools import chain
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.contrib.auth.decorators import login_required

from .helpers.ChatHelper import ChatHelper
from .models import Product, Order, Room, Message
from django.contrib.auth.models import User, Group

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


@login_required
def create_order(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        count = int(request.POST.get('count', 1))
        Order.objects.create(user=request.user, item=product, count=count, total_price=product.price*count, paid=False)
        return redirect('order_list')
    return render(request, 'create_order.html', {'product': product})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user, paid=0)
    return render(request, 'order_list.html', {'orders': orders})


@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')

        if name and price and description:
            Product.objects.create(
                user=request.user,
                name=name,
                price=price,
                description=description
            )
            return redirect('product_list')
    return render(request, 'add_product.html')


@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id, user=request.user)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        product.save()
        return redirect('user_products')
    return render(request, 'edit_product.html', {'product': product})


@login_required
def user_products(request):
    products = Product.objects.filter(user=request.user)
    return render(request, 'user_products.html', {'products': products})


def rooms(request):
    rooms = list(chain(Room.objects.filter(client=request.user), Room.objects.filter(manager=request.user)))
    return render(request, "rooms.html", {"rooms": rooms})


def room(request, slug):
    try:
        room = Room.objects.get(slug=slug)
        messages = Message.objects.filter(room=room)
    except Exception as e:
        print(e)
        redirect('product_list')
    return render(request, "room.html", {"room": room, "slug": slug, 'messages': messages})


def create_chat(request):
    if not request.user.is_authenticated or request.user.groups.filter(name='manager').exists() or request.user.is_superuser:
        return redirect('product_list')
    else:
        ChatHelper().create_room(request.user)
        return redirect('rooms')


