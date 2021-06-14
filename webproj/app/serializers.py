from app.models import *
from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ('id', 'name', 'discount', 'description', 'deadline')

class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
            else:
                raise serializers.ValidationError()

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                raise serializers.ValidationError()

            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            file_extension = imghdr.what(file_name, decoded_file)
            file_extension = "jpg" if file_extension == "jpeg" else file_extension
            complete_file_name = "%s.%s" % (file_name, file_extension,)

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)


class ProductSerializer(serializers.ModelSerializer):
    promotion = PromotionSerializer()
    image = serializers.SerializerMethodField('get_image_url')
    conditions = ['New', 'Used']

    def get_image_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image.url)

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'description', 'quantity', 'stock', 'brand', 'category', 'promotion', 'date',
                  'conditions', 'condition', 'image')



class SoldSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    promotion = PromotionSerializer()

    class Meta:
        model = Sold
        fields = ('id', 'product', 'quantity', 'buyer', 'date', 'buyer', 'promotion', 'total')


class CommentSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

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
    method = PaymentMethodSerializer()
    shopping_cart = ShoppingCartSerializer()

    class Meta:
        model = Payment
        fields = ('id', 'address', 'total', 'date', 'method', 'shopping_cart', 'usedCredits', 'username')


class ShoppingCartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ShoppingCartItem
        fields = ('id', 'quantity', 'cart_id', 'product')
