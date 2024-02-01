from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'users', UserViewSet, basename='user')
router.register(r'orders', OrderViewSet, basename='order')


# The API URLs are now determined automatically by the router.
urlpatterns = router.urls

urlpatterns += [
    path('create_tron_wallet/', CreateTronWallet.as_view(), name="create_tron_wallet"),
    path('create_eth_wallet/', CreateEthWallet.as_view(), name="create_eth_wallet"),
    path('send_trx/<str:pk>/<int:amount>/<str:rec_address>', CreateTrxTransaction.as_view(), name="send_trx"),
    path('send_trc20/<str:pk>/<int:amount>/<str:rec_address>', CreateTrc20Transaction.as_view(), name="send_trc20"),
    path('send_eth/<str:pk>/<str:amount>/<str:rec_address>', CreateEthTransaction.as_view(), name="send_eth"),
    path('send_erc20/<str:pk>/<str:amount>/<str:rec_address>', CreateErc20Transaction.as_view(), name="send_erc20"),
]
