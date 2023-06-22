from rest_framework import serializers
from adminapp.models import Category, Product, ProductPrice, Cart, Order

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'image', 'availability']

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= Product
#         fields = ['id', 'name', 'category', 'image', 'description', 'availability']
        
# class ProductPriceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductPrice
#         fields = ['id', 'product', 'name', 'actual_price', 'discount_price', 'tax']
        





class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'availability']

class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ['id', 'name', 'actual_price', 'discount_price', 'tax']

class ProductSerializer(serializers.ModelSerializer):
    prices = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'image', 'description', 'availability', 'prices']

    def get_prices(self, obj):
        prices = obj.productprice_set.all()
        serializer = ProductPriceSerializer(prices, many=True)
        return serializer.data





class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'product_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'order_items', 'reference_number', 'order_type', 'name', 'whatsapp_number', 'contact_number', 'address_one', 'address_two', 'address_three', 'order_note', 'payment_mode', 'date', 'time', 'canceled']
