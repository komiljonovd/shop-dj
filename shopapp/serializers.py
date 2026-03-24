from rest_framework import serializers
from .models import Product,Cart,Order

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['created_at','updated_at']


class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'product', 'product_name', 'quantity', 'total_price']
        read_only_fields = ['id']

    def get_total_price(self, obj):
        return obj.quantity * obj.product.price

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Количество должно быть больше 0")
        return value


# 📦 Order
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'total', 'status', 'created_at']