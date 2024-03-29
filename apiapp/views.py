from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import ProductSerializer, ProductPriceSerializer

from django.conf import settings
import static


# ------------------------------------------ Category ----------------------------------------------------------- #
@api_view(['GET', 'POST'])
def category_list_api(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




# class CategoryProductsAPIView(APIView):
#     def get(self, request, category_id):
#         category = Category.objects.get(id=category_id)
#         products = category.product_set.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)

class CategoryProductsAPIView(APIView):
    def get(self, request, category_id):
        category = Category.objects.get(id=category_id)
        products = category.product_set.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)



# --------------------------------------------------- Products ----------------------------------------------------------- #


# @api_view(['GET', 'POST'])
# def product_list_api(request):
#     if request.method == 'GET':
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def product_list_api(request):
#     if request.method == 'GET':
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)

#         response_data = []

#         for product in products:
#             product_data = next((item for item in serializer.data if item['id'] == product.id), None)

#             product_price = ProductPrice.objects.filter(product=product).first()
#             if product_price:
#                 product_price_serializer = ProductPriceSerializer(product_price)
#                 price_data = product_price_serializer.data
#                 product_data['price'] = price_data

#             response_data.append(product_data)

#         return Response(response_data)


@api_view(['GET'])
def product_list_api(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        response_data = []

        for product in products:
            product_data = next((item for item in serializer.data if item['id'] == product.id), None)

            product_prices = ProductPrice.objects.filter(product=product)
            if product_prices:
                product_price_serializer = ProductPriceSerializer(product_prices, many=True)
                price_data = product_price_serializer.data
                product_data['prices'] = price_data

            response_data.append(product_data)

        return Response(response_data)




# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail_api(request, pk):
#     try:
#         product = Product.objects.get(pk=pk)
#     except Product.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         product_prices = ProductPrice.objects.filter(product__id=pk)
        
#         varients = ProductPriceSerializer(product_prices,many=True)
        
#         data = [serializer.data,varients.data]
        
#         array = {'product':data[0],'varients':data[1]}
        
#         return Response(array)

    # elif request.method == 'PUT':
    #     serializer = ProductSerializer(product, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # elif request.method == 'DELETE':
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        product_prices = ProductPrice.objects.filter(product__id=pk)
        
        varients = ProductPriceSerializer(product_prices, many=True)
        
        response_data = {
            "product": serializer.data,
            "variants": varients.data
        }
        
        return Response(response_data)
    
    
class ProductDetailAPI(APIView):
    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        product_prices = product.productprice_set.all()

        # Calculate actual prices with tax and discount prices with tax for each product price
        for price in product_prices:
            price.actual_price_with_tax = price.calculate_actual_price_with_tax()
            price.discount_price_with_tax = price.calculate_discount_price_with_tax()

        product_serializer = ProductSerializer(product)
        prices_serializer = ProductPriceSerializer(product_prices, many=True)

        data = {
            'product': product_serializer.data,
            'product_prices': prices_serializer.data
        }

        return Response(data)


# --------------------------------------------------- ProductPrice ----------------------------------------------------------- #


@api_view(['GET', 'POST'])
def product_price_list_api(request):
    if request.method == 'GET':
        product_prices = ProductPrice.objects.all()
        serializer = ProductPriceSerializer(product_prices, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductPriceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def product_price_detail_api(request, pk):
    try:
        product_price = ProductPrice.objects.get(pk=pk)
    except ProductPrice.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductPriceSerializer(product_price)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductPriceSerializer(product_price, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product_price.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






# --------------------------------------------- User ----------------------------------------------------------- #

@api_view(['GET', 'POST'])
def user_list_api(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_api(request):
    if request.metho == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)





# -------------------------------------------------- Cart ------------------------------------------------------------ #

# @api_view(['GET', 'POST'])
# def cart_list_api(request):
#     if request.method == 'GET':
#         user_id = request.GET.get('user_id')  
#         cart_items = Cart.objects.filter(user__user_id=user_id)
#         serializer = CartSerializer(cart_items, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = CartSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# @api_view(['GET', 'POST'])
# def my_carts_api(request):
#     if request.method == 'GET':
#         carts = Cart.objects.all()
#         users = User.objects.all()
#         serializer = CartSerializer(carts, many=True)
#         userserializer = UserSerializer(users, many=True)
        
#         response_data = {
#             "user": userserializer.data,
#             "carts": serializer.data
#         }
        
#         return Response(response_data)

#     elif request.method == 'POST':
#         serializer = CartSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def my_carts_api(request):
    if request.method == 'GET':
        carts = Cart.objects.all()
        users = User.objects.all()
        serializer = CartSerializer(carts, many=True)
        userserializer = UserSerializer(users, many=True)
        
        response_data = {
            "user": userserializer.data,
            "carts": serializer.data
        }
        
        return Response(response_data)

    elif request.method == 'POST':
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            product_price = serializer.validated_data['product_price']
            user = serializer.validated_data['user']

            # Check if the same product already exists in the cart for the user
            existing_cart = Cart.objects.filter(user=user, product_price=product_price).first()
            if existing_cart:
                existing_cart.quantity += 1
                existing_cart.save()
                return Response(CartSerializer(existing_cart).data, status=status.HTTP_200_OK)
            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['GET'])
# def cart_items_view(request):
#     user_id = request.GET.get('user_id')
    
#     try:
#         user = User.objects.get(user_id=user_id)
#     except User.DoesNotExist:
#         return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    
#     cart_items = Cart.objects.filter(user=user) 
    
#     cart_item_data = []
#     for item in cart_items:
#         cart_item_data.append({
#             'id': item.id,
#             'product_name': item.product_price.product.name,
#             'product_price': item.product_price_dummy,
#             'tax': item.tax_dummy,
#             'quantity': item.quantity,
#             'total': str(item.total),
#         })
#     return Response(cart_item_data)

# @api_view(['GET'])
# def cart_items_view():    
#     cart_items = Cart.objects.all()
#     cart_item_data = []
#     for item in cart_items:
#         cart_item_data.append({
#             'id': item.id,
#             'user': item.user,
#             'product_name': item.product_price.product.name,
#             'product_variant': item.product_price.name,
#             'product_price': item.product_price_dummy,
#             'tax': item.tax_dummy,
#             'quantity': item.quantity,
#             'total': str(item.total),
#         })
#     return Response(cart_item_data)



# @api_view(['GET', 'PUT'])
# def cart_items_view(request):
#     if request.method == 'GET':
#         cart_items = Cart.objects.all()
#         cart_item_data = []
#         for item in cart_items:
#             image_path = item.product_price.product.image.url if item.product_price.product.image else None
#             image_url = image_path if image_path else static(settings.MEDIA_URL + 'default_image.jpg')
#             cart_item_data.append({
#                 'id': item.id,
#                 'user': item.user,
#                 'product_name': item.product_price.product.name,
#                 'image': image_url,
#                 'product_variant': item.product_price.name,
#                 'product_price': item.product_price_dummy,
#                 'tax': item.tax_dummy,
#                 'quantity': item.quantity,
#                 'total': str(item.total),
#             })
#         return Response(cart_item_data)
    
#     elif request.method == 'PUT':
#         cart_items = Cart.objects.all()
#         cart_item_data = []
#         for item in cart_items:
#             item.quantity = request.data.get('quantity', item.quantity)
#             item.save()
#             cart_item_data.append({
#                 'id': item.id,
#                 'user': item.user,
#                 'product_name': item.product_price.product.name,
#                 'product_variant': item.product_price.name,
#                 'product_price': item.product_price_dummy,
#                 'tax': item.tax_dummy,
#                 'quantity': item.quantity,
#                 'total': str(item.total),
#             })
#         return Response(cart_item_data)
    

from decimal import Decimal

@api_view(['GET', 'PUT', 'DELETE'])
def cart_items_view(request):
    if request.method == 'GET':
        cart_items = Cart.objects.all()
        cart_item_data = []
        for item in cart_items:
            
            
            product_price_total = Decimal(item.product_price_dummy) * Decimal(item.quantity)
            
            image_path = item.product_price.product.image.url if item.product_price.product.image else None
            image_url = image_path if image_path else static(settings.MEDIA_URL + 'default_image.jpg')
            cart_item_data.append({
                'id': item.id,
                'user': item.user,
                'product_name': item.product_price.product.name,
                'image': image_url,
                'product_variant': item.product_price.name,
                'product_price': item.product_price_dummy,
                'quantity': item.quantity,
                'product_price_total' : product_price_total,
                'tax': item.tax_dummy,
                'total': str(item.total),
                
            })
        return Response(cart_item_data)

    elif request.method == 'PUT':
        cart_items = Cart.objects.all()
        cart_item_data = []
        for item in cart_items:
            item.quantity = request.data.get('quantity', item.quantity)
            item.save()
            cart_item_data.append({
                'id': item.id,
                'user': item.user,
                'product_name': item.product_price.product.name,
                'product_variant': item.product_price.name,
                'product_price': item.product_price_dummy,
                'tax': item.tax_dummy,
                'quantity': item.quantity,
                
            })
        return Response(cart_item_data)

    elif request.method == 'DELETE':
        cart_items = Cart.objects.all()
        for item in cart_items:
            item.delete()
        return Response({'message': 'Cart items deleted successfully.'})

    
@api_view(['GET', 'PUT', 'DELETE'])
def cart_detail_api(request, pk):
    try:
        cart_item = Cart.objects.get(pk=pk)
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CartSerializer(cart_item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CartSerializer(cart_item, data={'quantity': request.data.get('quantity')}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET'])
# def cart_count(request):
#     user_uuid = request.user.pk  # Assuming request.user is a User instance
#     cart_count = Cart.objects.filter(user=user_uuid).count()
#     data = {'cart_count': cart_count}
#     return Response(data)



# ----------------------------------------------------------------- Order ------------------------------------------------------ #


@api_view(['GET', 'POST'])
def order_type_api(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderTypeSerializer(orders, many=True)
        serialized_data = serializer.data
        for i, order_data in enumerate(serialized_data):
            order_data['id'] = orders[i].id  # Add the 'id' field to each order data
        return Response(serialized_data)

    elif request.method == 'POST':
        data = {
            'order_type': request.data.get('order_type'),
            'cart': request.data.get('cart')
        }
        serializer = OrderTypeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def order_detail_api(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
# @api_view(['GET', 'POST'])
# def order_item_list_api(request):
#     if request.method == 'GET':
#         order_items = Cart.objects.all()
#         serializer = CartSerializer(order_items, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = CartSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# @api_view(['GET', 'PUT', 'DELETE'])
# def order_item_detail_api(request, pk):
#     try:
#         order_item = Cart.objects.get(pk=pk)
#     except Cart.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = CartSerializer(order_item)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = CartSerializer(order_item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         order_item.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
def order_list_api(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






