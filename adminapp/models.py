from django.db import models
from decimal import Decimal

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
        if self.discount_price is not None:  # Check if discount price is available
            price = self.discount_price
        else:
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
    name = models.CharField(max_length=100,null=True)
    ip = models.GenericIPAddressField()
    user_id = models.CharField(max_length=225)
    def __str__(self):
        return self.name

# ------------------------------------------------- Cart ---------------------------------------------------------------------- #

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_price = models.ForeignKey(ProductPrice, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.user.name
    
    
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
    cart = models.ManyToManyField(Cart)
    reference_number = models.CharField(max_length=100, unique=True)
    order_type = models.CharField(max_length=100, choices=TYPE)
    name = models.CharField(max_length=200)
    whatsapp_number = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=20)
    address_one = models.CharField(max_length=500)
    address_two = models.CharField(max_length=500)
    address_three = models.CharField(max_length=500)
    order_note = models.CharField(max_length=500)
    payment_mode = models.CharField(max_length=100, choices=PAYMENT_MODE)
    date = models.DateField()
    time = models.TimeField()
    canceled = models.BooleanField(default=False)

    def get_product_total_price(self):
        total_price = Decimal(0)
        for order_item in self.cart.all():
            total_price += order_item.get_total_price_with_tax()
        return total_price

# ------------------------------------------------- Table ---------------------------------------------------------------------- #

class Table(models.Model):
    table_number = models.CharField(max_length=10)
    seating_capacity = models.PositiveIntegerField()
    is_occupied = models.BooleanField(default=False)
    cart = models.ManyToManyField(Cart)
    def __str__(self):
        return self.table_number
