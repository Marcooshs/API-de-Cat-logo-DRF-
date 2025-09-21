from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source= 'product.name')
    sku = serializers.ReadOnlyField(source= 'product.sku')
    line_total = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'sku', 'product_name', 'quantity', 'unit_price', 'line_total']
        read_only_fields = ['id', 'sku', 'product_name', 'unit_price', 'line_total']

    @staticmethod
    def get_line_total(obj):
        return obj.unit_price * obj.quantity

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many= True, read_only= True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'total_amount', 'shipping_address', 'created_at', 'updated_at', 'items']
        read_only_fields = ['id', 'status', 'total_amount', 'created_at', 'updated_at', 'items']

class AdminOrderSerializer(OrderSerializer):
    class Meta(OrderSerializer.Meta):
        read_only_fields = ['id', 'total_amount', 'created_at', 'updated_at', 'items']
