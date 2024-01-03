from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.CharField(max_length=255)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
    total_price = models.IntegerField()
    paid = models.BooleanField()


class Card(models.Model):
    number = models.IntegerField()
    date = models.CharField(max_length=5)
    cvv = models.IntegerField()



