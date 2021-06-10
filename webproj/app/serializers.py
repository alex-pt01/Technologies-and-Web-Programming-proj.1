from app.models import *
from rest_framework import serializers


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ('id', 'name', 'discount', 'description', 'deadline')


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'description', 'quantity', 'stock', 'brand', 'category', 'promotion', 'date',
                  'conditions', 'condition', 'image')


class SoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sold
        fields = ('id', 'product', 'quantity', 'buyer', 'date', 'buyer', 'promotion', 'total')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'userName', 'userEmail', 'description', 'rating', 'commentDate', 'product')


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ('id', 'type', 'card_no')


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('id', 'user_id')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'address', 'total', 'date', 'method', 'shopping_cart', 'usedCredits', 'username')


class ShoppingCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCartItem
        fields = ('id', 'quantity', 'cart_id', 'product')
