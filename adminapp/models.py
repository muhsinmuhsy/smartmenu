from django.db import models

from decimal import Decimal

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db.models.signals import pre_delete

import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

# Create your models here.

# ------------------------------------------------- Category ---------------------------------------------------------------------- #

class Category(models.Model):
    name = models.CharField(max_length= 100)
    image = models.ImageField(upload_to='category_image', null=True)
    availability = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
# ------------------------------------------------- Product ---------------------------------------------------------------------- #

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='product_image', null=True)
    description = models.CharField(max_length=100, null=True)
    availability = models.BooleanField(default=False)
    def __str__(self):
        return self.name

@receiver(pre_delete, sender=Category)
def delete_related_products(sender, instance, **kwargs):
    instance.product_set.all().delete() 
# ------------------------------------------------- Product Price ---------------------------------------------------------------------- #
    
class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    actual_price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)  
    tax = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return f"{self.product} ({self.name})"

    def calculate_actual_price_with_tax(self):
        
        price = self.actual_price

        tax_amount = Decimal(price) * Decimal(self.tax) / 100
        actual_price_with_tax = Decimal(price) + tax_amount
        return actual_price_with_tax

    def calculate_discount_price_with_tax(self):
        if self.discount_price is not None:  # Check if discount price is available
            price = self.discount_price
        else:
            price = self.actual_price

        tax_amount = Decimal(price) * Decimal(self.tax) / 100
        discount_price_with_tax = Decimal(price) + tax_amount
        return discount_price_with_tax

# ------------------------------------------------- User ---------------------------------------------------------------------- #

class User(models.Model):
    user_id = models.UUIDField()
    def __str__(self):
        return self.user_id
    
   

    def save(self, *args, **kwargs):
        existing_user = User.objects.filter(user_id=self.user_id).first()
        if existing_user:
            return  # Don't save if a user with the same name already exists
        super().save(*args, **kwargs)
        
        
        
# ------------------------------------------------- Table ---------------------------------------------------------------------- #

class Table(models.Model):
    table_number = models.CharField(max_length=10, unique=True)
    seating_capacity = models.PositiveIntegerField()
    is_occupied = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    
    def __str__(self):
        return self.table_number

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.table_number)
        canvas = Image.new('RGB', (290, 290), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.table_number}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)
        
        

# ------------------------------------------------- Cart ---------------------------------------------------------------------- #


class Cart(models.Model):
    user = models.UUIDField(null=True, blank=True)
    # table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True, blank=True)
    product_price = models.ForeignKey(ProductPrice, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    product_price_dummy = models.CharField(max_length=100, null=True, blank=True)
    tax_dummy = models.CharField(max_length=100, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # def __str__(self):
    #     return self.user.user_id
    
    # def __str__(self):
    #     return self.product_price.name
    
    def __str__(self):
        return f"Cart {self.id} - User: {self.user}"
    
    def save(self, *args, **kwargs):
        if self.product_price.discount_price is not None:
            price = self.product_price.discount_price
        else:
            price = self.product_price.actual_price

        tax_amount = Decimal(price) * Decimal(self.product_price.tax) / 100
        total_price_with_tax = (Decimal(price) + tax_amount) * Decimal(self.quantity)
        self.total = total_price_with_tax

        super().save(*args, **kwargs)
        
    # ITEMS TOTAL PRICE (TOTAL ITEM WITH TAX WITH QUANTITY TOTAL )
    def get_total_price_with_tax(self):
        if self.product_price.discount_price is not None:
            price = self.product_price.discount_price
        else:
            price = self.product_price.actual_price

        tax_amount = Decimal(price) * Decimal(self.product_price.tax) / 100
        total_price_with_tax = (Decimal(price) + tax_amount) * Decimal(self.quantity)
        return total_price_with_tax
    
    # ONE ONE ITEM WITH QUANTITYS WITH TOTAL
    def get_total_tax_with_price_and_quantity(self):
        if self.product_price.discount_price is not None:
            price = self.product_price.discount_price
        else:
            price = self.product_price.actual_price

        tax_amount = Decimal(price) * Decimal(self.product_price.tax) / 100
        total_tax_with_price_and_quantity = (tax_amount + Decimal(price)) * Decimal(self.quantity)
        return total_tax_with_price_and_quantity


    # -- DUMMY CALCULATES -- #
    def get_total_price_with_tax_dummy(self):
        price = self.product_price_dummy
        tax_amount = Decimal(price) * Decimal(self.tax_dummy) / 100
        total_price_with_tax = (Decimal(price) + tax_amount) 
        return total_price_with_tax

    def get_total_tax_with_price_and_quantity_dummy(self):
        price = self.product_price_dummy
        tax_amount = Decimal(price) * Decimal(self.tax_dummy) / 100
        total_tax_with_price_and_quantity = (tax_amount + Decimal(price)) * Decimal(self.quantity)
        return total_tax_with_price_and_quantity


# -- AUTO SAVE THE DUMMY FIELD -- #
@receiver(post_save, sender=Cart)
def update_cart_total(sender, instance, created, **kwargs):
    if created:
        if instance.product_price.discount_price is not None:
            price = instance.product_price.discount_price
        else:
            price = instance.product_price.actual_price

        tax_amount = Decimal(price) * Decimal(instance.product_price.tax) / 100
        total_price_with_tax = (Decimal(price) + tax_amount) * Decimal(instance.quantity)
        instance.total = total_price_with_tax

        # Save discount_price if available, otherwise save actual_price
        if instance.product_price.discount_price is not None:
            instance.product_price_dummy = instance.product_price.discount_price
        else:
            instance.product_price_dummy = instance.product_price.actual_price

        # Save tax value
        instance.tax_dummy = instance.product_price.tax

        instance.save()


    
    
  
# ------------------------------------------------- Order---------------------------------------------------------------------- #

class Order(models.Model):
    TYPE = (
        ('Home Delivery', 'Home Delivery'),
        ('Take Away', 'Take Away'),
    )
    PAYMENT_MODE = (
        ('Cash on Delivery', 'Cash on Delivery'),
        ('Card on Delivery', 'Card on Delivery'),
    )
    STATUS = (
        ('Pending', 'Pending'),
        ('Order Confirmed', 'Order Confirmed'),
        ('Order Don', 'Order Don'),
        ('Cancel', 'Cancel'),          
    )
    cart = models.ManyToManyField(Cart)
    reference_number = models.CharField(max_length=100)
    order_type = models.CharField(max_length=100, choices=TYPE)
    name = models.CharField(max_length=200)
    whatsapp_number = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=20)
    address_one = models.CharField(max_length=500)
    address_two = models.CharField(max_length=500)
    address_three = models.CharField(max_length=500)
    order_note = models.CharField(max_length=500)
    payment_mode = models.CharField(max_length=100, choices=PAYMENT_MODE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS, default='Pending', null=True, blank=True)
    confirm = models.BooleanField(default=False, null=True, blank=True)
    def get_product_total_price(self):
        total_price = Decimal(0)
        for order_item in self.cart.all():
            total_price += order_item.get_total_price_with_tax()
        return total_price
    
    # -- For Dummy -- #
    def get_cart_total(self):
        total = Decimal(0)
        for cart_item in self.cart.all():
            total += cart_item.total
        return total

        