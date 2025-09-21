from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']

class ProductSerializer(serializers.ModelSerializer):
    # nome da categoria como somente leitura
    category_name = serializers.ReadOnlyField(source= 'category.name')

    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'price', 'stock', 'is_active', 'category', 'category_name']
        read_only_fields = ['id', 'category_name']
