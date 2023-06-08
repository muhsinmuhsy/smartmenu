from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length= 100)
    image = models.ImageField(upload_to='category_image', null=True)
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='product_image', null=True)
    description = models.CharField(max_length=100)
    availability = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    actual_price = models.IntegerField()
    discount_price = models.IntegerField()