from django.http import JsonResponse
from rest_framework import viewsets
from apps.website.models import Order, Product
from django.contrib.auth.models import User
from .serializers import UserSerializer, ProductSerializer, OrderSerializer
from ..trongrid.views import create_tron_account, send_trc20, send_trx


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer


def create_tron_wallet(request):
    if request.method == 'GET':
        wallet = create_tron_account()
        return JsonResponse({"address": wallet['address'], "private_key": wallet['private_key']}, safe=False)


def create_trx_transaction(request, pk, amount, rec_address):
    if request.method == 'GET':
        res = send_trx(pk, amount, rec_address)
        response_data = {
            'transaction_data': str(res),
        }
        print(res)
        return JsonResponse(response_data)


def create_trc20_transaction(request, pk, amount, rec_address):
    if request.method == 'GET':
        res = send_trc20(pk, amount, rec_address)
        response_data = {
            'transaction_data': str(res),
        }
        print(res)
        return JsonResponse(response_data)

