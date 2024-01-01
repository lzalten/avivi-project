from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, UserViewSet, OrderViewSet

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'users', UserViewSet, basename='user')
router.register(r'orders', OrderViewSet,basename='order')


# The API URLs are now determined automatically by the router.
urlpatterns = router.urls