from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def admin_index(request):
    return render(request, 'admin_index.html')

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
        
        # Save only the original image
        category = Category(name=name, image=image)
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
        discount_price = request.POST.get('discount_price')
        
        

        # Create the main product price
        product_price = ProductPrice.objects.create(
            product=product,
            name=price_name,
            actual_price=actual_price,
            discount_price=discount_price,
            
        )

        # Get the additional product price data
        additional_price_names = request.POST.getlist('additional_price_name[]')
        additional_actual_prices = request.POST.getlist('additional_actual_price[]')
        additional_discount_prices = request.POST.getlist('additional_discount_price[]')
        

        # Create additional product prices
        for i in range(len(additional_price_names)):
            additional_price = ProductPrice.objects.create(
                product=product,
                name=additional_price_names[i],
                actual_price=additional_actual_prices[i],
                discount_price=additional_discount_prices[i],
                
            )

        return redirect('product_list')  # Replace 'product_list' with the appropriate URL name

    # Handle the case when the request method is not POST
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
        discount_price = request.POST.get('discount_price')

        try:
            product_price, created = ProductPrice.objects.update_or_create(
                product=product,
                defaults={
                    'name': price_name,
                    'actual_price': actual_price,
                    'discount_price': discount_price,
                }
            )
        except ProductPrice.MultipleObjectsReturned:
            # Multiple ProductPrice objects found, select the first one
            product_price = product.productprice_set.first()
            product_price.name = price_name
            product_price.actual_price = actual_price
            product_price.discount_price = discount_price
            product_price.save()

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
                additional_price.discount_price = discount_price
                additional_price.save()
            else:  # Otherwise, create a new additional price
                additional_price = ProductPrice.objects.create(
                    product=product,
                    name=price_name,
                    actual_price=actual_price,
                    discount_price=discount_price,
                )

        return redirect('product_list')  # Replace 'product_list' with the appropriate URL name

    # Handle the case when the request method is not POST
    categories = Category.objects.all()  # Assuming you have a Category model
    return render(request, 'edit_product.html', {'product': product, 'product_price': product_price, 'categories': categories})



@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product_prices = product.productprice_set.all()  # Retrieve all product prices associated with the product
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


# ---------------------- For product avalability toggle on/of switch --------------------#

def toggle_availability(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.availability = not product.availability
    product.save()
    return JsonResponse({'success': True})