
from django.urls import path,include
from .views import ProductApi,CartApi, CartDeleteApi, OrderApi

urlpatterns= [
    path('',ProductApi.as_view(),name='product-post-get'),
    path('cart/', CartApi.as_view()),
    path('cart/<int:pk>/', CartDeleteApi.as_view()),
    path('orders/', OrderApi.as_view()),
]