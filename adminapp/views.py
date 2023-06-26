from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from datetime import date
from django.http import HttpResponse

# Create your views here.



# @login_required
# def admin_index(request):
#     today = date.today()  # Get today's date

#     # Filter the orders for today excluding canceled orders
#     orders = Order.objects.filter(date=today, canceled=False)

#     total_orders_count = orders.count()  # Fetch the count of orders for today

#     canceled_orders_count = Order.objects.filter(date=today, canceled=True).count()  # Fetch the count of canceled orders for today

#     # Calculate the total earnings for today
#     total_earnings = Decimal(0)
#     for order in orders:
#         total_earnings += order.get_product_total_price()

#     if request.method == 'POST':
#         order_id = request.POST.get('order_id')
#         order = Order.objects.get(id=order_id)
#         order.canceled = True
#         order.save()
#         return HttpResponse(status=204)  # Return a success response

#     order_types = []
#     for order_type in Order.TYPE:
#         count = orders.filter(order_type=order_type[0]).count()
#         order_types.append((order_type[0], order_type[1], count))

#     context = {
#         'orders': orders,
#         'total_orders_count': total_orders_count,
#         'canceled_orders_count': canceled_orders_count,
#         'order_types': order_types,
#         'total_earnings': total_earnings,
#     }
#     return render(request, 'admin_index.html', context)



@login_required
def admin_index(request):
    tables = Table.objects.all()
    today = date.today()  # Get today's date

    # Filter the orders for today
    orders = Order.objects.filter(date=today)

    # Calculate the total orders count for today
    total_orders_count = orders.count()

    # Filter the canceled orders for today
    canceled_orders = orders.filter(status='Canceled')

    # Calculate the count of canceled orders
    canceled_orders_count = canceled_orders.count()

    # Filter the orders with status 'Order Don' for today
    orders_don = orders.filter(status='Order Don')

    # Calculate the total cart earnings for the orders with status 'Order Don'
    total_cart_earnings = Decimal(0)
    for order in orders_don:
        total_cart_earnings += order.get_cart_total()

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')
        order = Order.objects.get(id=order_id)
        order.status = status
        order.save()
        return HttpResponse(status=204)  # Return a success response

    order_types = []
    for order_type in Order.TYPE:
        count = orders.filter(order_type=order_type[0]).count()
        order_types.append((order_type[0], order_type[1], count))

    context = {
        'tables' : tables,
        'orders': orders,
        'total_orders_count': total_orders_count,
        'canceled_orders_count': canceled_orders_count,
        'total_cart_earnings': total_cart_earnings,
        'order_types': order_types,
    }
    return render(request, 'admin_index.html', context)



def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_details.html', {'order': order})



def type_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    return render(request, 'type_details.html', context)


# --------------------------- Category ---------------------------------------------- #

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


@login_required
def category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        availability = request.POST.get('availability') == 'on'
        
        # Save only the original image
        category = Category(name=name, image=image,availability=availability)
        category.save()
        
        return redirect('category_list')
    
    return render(request, 'category_add.html')


@login_required
def category_products(request, category_id):
    category = Category.objects.get(id=category_id)
    products = category.product_set.all()
    return render(request, 'category_products.html', {'category': category, 'products': products})


@login_required
def category_edit(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.image = request.FILES.get('image')
        category.save()
        return redirect('category_list')
    
    return render(request, 'category_edit.html', {'category': category})


@login_required
def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('category_list')

# ------------------------------ Product ----------------------------- #

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})



@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_ids = request.POST.getlist('category')
        image = request.FILES.get('image')
        description = request.POST.get('description')
        availability = request.POST.get('availability') == 'on'

        # Create the product
        categories = Category.objects.filter(id__in=category_ids)
        product = Product.objects.create(
            name=name,
            image=image,
            description=description,
            availability=availability
        )
        product.category.set(categories)

        # Get the product price data
        price_name = request.POST.get('price_name')
        actual_price = request.POST.get('actual_price')
        tax = request.POST.get('tax')

        # Check if discount price is provided
        discount_price = request.POST.get('discount_price')

        # Create the main product price
        product_price = ProductPrice.objects.create(
            product=product,
            name=price_name,
            actual_price=actual_price,
            tax=tax,
        )

        # Set the discount price if provided
        if discount_price:
            product_price.discount_price = discount_price
            product_price.save()

        # Get the additional product price data
        additional_price_names = request.POST.getlist('additional_price_name[]')
        additional_actual_prices = request.POST.getlist('additional_actual_price[]')
        additional_discount_prices = request.POST.getlist('additional_discount_price[]')
        additional_taxs = request.POST.getlist('additional_tax[]')

        # Create additional product prices
        for i in range(len(additional_price_names)):
            additional_price = ProductPrice.objects.create(
                product=product,
                name=additional_price_names[i] if additional_price_names[i] else None,
                actual_price=additional_actual_prices[i]if additional_actual_prices[i] else None,
                discount_price=additional_discount_prices[i] if additional_discount_prices[i] else None,
                tax=additional_taxs[i] if additional_taxs[i] else None,
            )

        return redirect('product_list')  # Replace 'product_list' with the appropriate URL name

    categories = Category.objects.all()  # Assuming you have a Category model
    return render(request, 'add_product.html', {'categories': categories})






@login_required
def edit_product(request, product_id):
    # Retrieve the product object based on the provided product_id
    product = Product.objects.get(id=product_id)

    # Retrieve the main product price associated with the product
    product_price = product.productprice_set.first()

    if request.method == 'POST':
        name = request.POST.get('name')
        category_ids = request.POST.getlist('category')
        image = request.FILES.get('image')
        description = request.POST.get('description')
        availability = request.POST.get('availability') == 'on'

        # Update the product with the new data
        product.name = name
        if image:
            product.image = image
        product.description = description
        product.availability = availability
        product.category.set(Category.objects.filter(id__in=category_ids))
        product.save()

        # Update or create the main product price
        price_name = request.POST.get('price_name')
        actual_price = request.POST.get('actual_price')
        tax = request.POST.get('tax')
        discount_price = request.POST.get('discount_price')

        if product_price:
            product_price.name = price_name
            product_price.actual_price = actual_price
            product_price.tax = tax

            if discount_price and discount_price != 'None':
                product_price.discount_price = float(discount_price)
            else:
                product_price.discount_price = None

            product_price.save()
        else:
            product_price = ProductPrice.objects.create(
                product=product,
                name=price_name,
                actual_price=actual_price,
                tax=tax,
                discount_price=float(discount_price) if discount_price and discount_price != 'None' else None,
            )

        # Get the additional product price data
        additional_price_ids = request.POST.getlist('additional_price_id[]')
        additional_price_names = request.POST.getlist('additional_price_name[]')
        additional_actual_prices = request.POST.getlist('additional_actual_price[]')
        additional_discount_prices = request.POST.getlist('additional_discount_price[]')

        # Update or create additional product prices
        for i in range(len(additional_price_ids)):
            price_id = additional_price_ids[i]
            price_name = additional_price_names[i]
            actual_price = additional_actual_prices[i]
            discount_price = additional_discount_prices[i]

            if price_id:  # If price_id is provided, update the existing price
                additional_price = ProductPrice.objects.get(id=price_id)
                additional_price.name = price_name
                additional_price.actual_price = actual_price

                if discount_price and discount_price != 'None':
                    additional_price.discount_price = float(discount_price)
                else:
                    additional_price.discount_price = None

                additional_price.save()
            else:  # Otherwise, create a new additional price
                additional_price = ProductPrice.objects.create(
                    product=product,
                    name=price_name,
                    actual_price=actual_price,
                    discount_price=float(discount_price) if discount_price and discount_price != 'None' else None,
                )

        return redirect('product_list')  # Replace 'product_list' with the appropriate URL name

    # Handle the case when the request method is not POST
    categories = Category.objects.all()  # Assuming you have a Category model
    return render(request, 'edit_product.html', {'product': product, 'product_price': product_price, 'categories': categories})





@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product_prices = product.productprice_set.all()

    # Calculate actual prices with tax and discount prices with tax for each product price
    for price in product_prices:
        price.actual_price_with_tax = price.calculate_actual_price_with_tax()
        price.discount_price_with_tax = price.calculate_discount_price_with_tax()

    return render(request, 'product_detail.html', {'product': product, 'product_prices': product_prices})



@login_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('product_list')


@login_required
def edit_product_image(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST' and 'image' in request.FILES:
        product.image = request.FILES['image']
        product.save()
        return redirect('product_detail', product_id=product_id)

    return render(request, 'edit_product_image.html', {'product': product})



# --------------------------------- Report ----------------------------------------- #




# def report(request):
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')
#     order_type = request.GET.get('order_type')

#     orders = Order.objects.all()

#     if start_date:
#         orders = orders.filter(date__gte=start_date)
#     if end_date:
#         orders = orders.filter(date__lte=end_date)
#     if order_type:
#         orders = orders.filter(order_type=order_type)

#     context = {
#         'orders': orders,
#         'start_date': start_date,  # Pass the start_date to the template
#         'end_date': end_date,      # Pass the end_date to the template
#         'order_type': order_type,  # Pass the order_type to the template
#     }

#     return render(request, 'report.html', context)

def report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    order_type = request.GET.get('order_type')

    orders = Order.objects.all()

    if start_date:
        orders = orders.filter(date__gte=start_date)
    if end_date:
        orders = orders.filter(date__lte=end_date)
    if order_type:
        orders = orders.filter(order_type=order_type)

    context = {
        'orders': orders,
        'start_date': start_date,
        'end_date': end_date,
        'order_type': order_type,
    }

    return render(request, 'report.html', context)


def report_detalis(request, order_id):
    order = Order.objects.get(id= order_id)
    return render(request, 'report_detalis.html', {'order': order})


# --------------------------------- Table ----------------------------------------- #



def table_list(request):
    tables = Table.objects.all()
    return render(request, 'table_list.html', {'tables': tables})

def table_create(request):
    if request.method == 'POST':
        table_number = request.POST['table_number']
        seating_capacity = request.POST['seating_capacity']
        is_occupied = request.POST.get('is_occupied', False) == 'on'
        table = Table.objects.create(table_number=table_number, seating_capacity=seating_capacity, is_occupied=is_occupied)
        return redirect('table_list')
    return render(request, 'table_create.html')

def table_update(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    if request.method == 'POST':
        table.table_number = request.POST['table_number']
        table.seating_capacity = request.POST['seating_capacity']
        table.is_occupied = request.POST.get('is_occupied', ) == 'on'
        table.save()
        return redirect('table_list')
    return render(request, 'table_update.html', {'table': table})


def table_delete(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    table.delete()
    return redirect('table_list')
 

# def table_status(request):
#     tables = Table.objects.all()
#     return render(request, 'table_status.html', {'tables': tables})

# def table_filter(request):
#     if request.method == 'GET':
#         query = request.GET.get('q')
#         if query:
#             tables = Table.objects.filter(table_number__icontains=query)
#         else:
#             tables = Table.objects.all()
#         return render(request, 'table_list.html', {'tables': tables})

# def table_sort(request):
#     sort_by = request.GET.get('sort_by')
#     if sort_by == 'table_number':
#         tables = Table.objects.order_by('table_number')
#     elif sort_by == 'seating_capacity':
#         tables = Table.objects.order_by('seating_capacity')
#     else:
#         tables = Table.objects.all()
#     return render(request, 'table_list.html', {'tables': tables})

# def table_assign(request, table_id, order_id):
#     table = get_object_or_404(Table, id=table_id)
#     order = get_object_or_404(Order, id=order_id)
    
#     table.order = order
#     table.is_occupied = True
#     table.save()
    
#     return redirect('table_list')



# ---------------------- For category, product avalability toggle on/of switch --------------------#

def toggle_availability(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.availability = not product.availability
    product.save()
    return JsonResponse({'success': True})



def toggle_category_availability(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.availability = not category.availability
    category.save()
    return JsonResponse({'success': True})



# ----------------------------------------------- cart --------------------------------------------------#


def add_to_cart(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        product_price_id = request.POST.get('product_price_id')
        quantity = request.POST.get('quantity')

        # Retrieve the corresponding User and ProductPrice objects
        user = User.objects.get(id=user_id)
        product_price = ProductPrice.objects.get(id=product_price_id)

        # Create a new Cart object
        cart = Cart(user=user, product_price=product_price, quantity=quantity)
        # Perform any additional logic or calculations here if needed
        cart.save()

        return redirect('admin_index')  # Redirect to a success page or another view

    # Retrieve the list of users and products to populate the dropdowns
    users = User.objects.all()  
    products = ProductPrice.objects.all()

    return render(request, 'add_to_cart.html', {'users': users, 'products': products})




