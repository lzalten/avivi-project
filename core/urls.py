from django.contrib import admin
from django.urls import path, include
from apps.website.views import *

urlpatterns = [
    path('', ProductList.as_view()),
    path('admin/', admin.site.urls, name='admin'),  # admin panel
    path('api/', include('apps.api.urls')),  # api urls
    path('website/', include('apps.website.urls')),  # website urls
]
