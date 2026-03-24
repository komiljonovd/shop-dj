from django.shortcuts import render
from rest_framework import generics, permissions, status
from .serializers import ProductSerializer
from .models import Product,Cart,Order
from .serializers import CartSerializer,OrderSerializer
from rest_framework.response import Response


# Create your views here.

class ProductApi(generics.ListCreateAPIView):
    serializer_class = ProductSerializer


    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [permissions.IsAdminUser]

        else:
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        return Product.objects.all()
    

class CartApi(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity', 1)

        cart_item = Cart.objects.filter(
            user=self.request.user,
            product=product
        ).first()

        if cart_item:
            # увеличиваем количество
            cart_item.quantity += quantity
            cart_item.save()
        else:
            serializer.save(user=self.request.user)


class CartDeleteApi(generics.DestroyAPIView):
    lookup_field = 'id'
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    


class OrderApi(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        if not cart_items.exists():
            return Response({"error": "Корзина пустая"}, status=400)

        # 💰 считаем total
        total = sum(item.product.price * item.quantity for item in cart_items)

        # создаём заказ
        order = Order.objects.create(user=user, total=total)

        # 🧹 очищаем корзину
        cart_items.delete()

        return Response({
            "message": "Заказ создан",
            "order_id": order.id,
            "total": total
        }, status=status.HTTP_201_CREATED)