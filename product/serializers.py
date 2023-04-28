from rest_framework import serializers
from .models import Product, Category, Cart


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["name"]


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'

class ProductFilterSerializer:

    class Meta:
        model = Product
        fields = ['price', 'name']
