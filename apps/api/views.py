from django.http import JsonResponse
from rest_framework import viewsets
from apps.website.models import Order, Product
from django.contrib.auth.models import User
from .serializers import UserSerializer, ProductSerializer, OrderSerializer
from ..blockchain.ethereum.EthereumHelper import EthereumHelper
from ..blockchain.tron.TronHelper import TronHelper
from django.views import View


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateTronWallet(View):
    def get(self, request):
        wallet = TronHelper().create_tron_wallet()
        return JsonResponse({"address": wallet['address'], "private_key": wallet['private_key']}, safe=False)


class CreateEthWallet(View):
    def get(self, request):
        wallet = EthereumHelper().create_ethereum_account()
        return JsonResponse({"address": wallet['address'], "private_key": wallet['private_key']}, safe=False)


class CreateTrxTransaction(View):
    def get(self, request, pk, amount, rec_address):
        res = TronHelper().send_trx(pk, amount, rec_address)
        response_data = {
            'transaction_data': str(res),
        }
        print(res)
        return JsonResponse(response_data)


class CreateTrc20Transaction(View):
    def get(self, request, pk, amount, rec_address):
        res = TronHelper().send_trc20(pk, amount, rec_address)
        response_data = {
            'transaction_data': str(res),
        }
        print(res)
        return JsonResponse(response_data)


class CreateEthTransaction(View):
    def get(self, request, pk, amount, rec_address):
        res = EthereumHelper().send_eth(pk, amount, rec_address)
        response_data = {
            'transaction_data': str(res),
        }
        print(res)
        return JsonResponse(response_data)


class CreateErc20Transaction(View):
    def get(self, request, pk, amount, rec_address):
        res = EthereumHelper().send_erc20(pk, amount, rec_address)
        response_data = {
            'transaction_data': str(res),
        }
        print(res)
        return JsonResponse(response_data)


