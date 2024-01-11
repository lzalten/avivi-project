from django.http import JsonResponse
from rest_framework import viewsets
from apps.website.models import Order, Product
from django.contrib.auth.models import User
from .serializers import UserSerializer, ProductSerializer, OrderSerializer
from ..blockchain.ethereum import EthereumHelper
from ..blockchain.tron import TronHelper


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
        wallet = TronHelper.create_tron_wallet()
        return JsonResponse({"address": wallet['address'], "private_key": wallet['private_key']}, safe=False)


def create_ethereum_wallet(request):
    if request.method == 'GET':
        wallet = EthereumHelper.create_ethereum_account()
        return JsonResponse({"address": wallet['address'], "private_key": wallet['private_key']}, safe=False)


def create_trx_transaction(request, pk, amount, rec_address):
    if request.method == 'GET':
        res = TronHelper.send_trx(pk, amount, rec_address)
        response_data = {
            'transaction_data': str(res),
        }
        print(res)
        return JsonResponse(response_data)


def create_trc20_transaction(request, pk, amount, rec_address):
    if request.method == 'GET':
        res = TronHelper.send_trc20(pk, amount, rec_address)
        response_data = {
            'transaction_data': str(res),
        }
        print(res)
        return JsonResponse(response_data)


def create_eth_transaction(request, pk, amount, rec_address):
    if request.method == 'GET':
        res = EthereumHelper.send_eth(pk, amount, rec_address)
        response_data = {
            'transaction_data': str(res),
        }
        print(res)
        return JsonResponse(response_data)


def create_erc20_transaction(request, pk, amount, rec_address):
    if request.method == 'GET':
        res = EthereumHelper.send_erc20(pk, amount, rec_address)
        response_data = {
            'transaction_data': str(res),
        }
        print(res)
        return JsonResponse(response_data)


