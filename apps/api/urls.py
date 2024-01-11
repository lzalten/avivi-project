from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, UserViewSet, OrderViewSet, create_tron_wallet, create_trx_transaction, \
    create_trc20_transaction, create_ethereum_wallet, create_eth_transaction, create_erc20_transaction

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'users', UserViewSet, basename='user')
router.register(r'orders', OrderViewSet, basename='order')


# The API URLs are now determined automatically by the router.
urlpatterns = router.urls

urlpatterns += [
    path('create_tron_wallet/', create_tron_wallet),
    path('create_eth_wallet/', create_ethereum_wallet),
    path('send_trx/<str:pk>/<int:amount>/<str:rec_address>', create_trx_transaction),
    path('send_trc20/<str:pk>/<int:amount>/<str:rec_address>', create_trc20_transaction),
    path('send_eth/<str:pk>/<str:amount>/<str:rec_address>', create_eth_transaction),
    path('send_erc20/<str:pk>/<str:amount>/<str:rec_address>', create_erc20_transaction),
]
