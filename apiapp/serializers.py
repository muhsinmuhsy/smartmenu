from rest_framework import serializers
from adminapp.models import Category, Product, ProductPrice, User, Cart, Order



# ------------------------------------------ --- Category ----------------------------------------------------------- #


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



# --------------------------------------------- Product Price ----------------------------------------------------------- #

class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ['id', 'name', 'actual_price', 'discount_price', 'tax']


# ------------------------------------------------ Product ----------------------------------------------------------- #

class ProductSerializer(serializers.ModelSerializer):
    
    prices = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'image', 'description', 'availability', 'prices']

    def get_prices(self, obj):
        prices = obj.productprice_set.all()
        serializer = ProductPriceSerializer(prices, many=True)
        return serializer.data

# ----------------------------------------------- User ----------------------------------------------------------- #

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'user_id', ]

# ---------------------------------------------- Cart ----------------------------------------------------------- #

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'product_price', 'quantity']

# -------------------------------------------- Order----------------------------------------------------------- #



class OrderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_type', 'cart']
        extra_kwargs = {
            'order_type': {'required': False},
            'cart': {'required': False},
        }


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        # fields = ['id', 'order_items', 'reference_number', 'order_type', 'name', 'whatsapp_number', 'contact_number', 'address_one', 'address_two', 'address_three', 'order_note', 'payment_mode', 'date', 'time', 'canceled']
        fields = '__all__'
