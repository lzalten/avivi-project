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


class Room(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=100)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client')
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manager')

    def __str__(self):
        return "Room : " + self.name + " | Id : " + self.slug


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        self.content
