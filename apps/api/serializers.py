from rest_framework import serializers
from apps.website.models import Product, Order
from django.contrib.auth.models import User


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user','item','count']
