from django.db import models
import uuid
from django.contrib.auth.models import User
class product_category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_image = models.ImageField(upload_to='category_image/',null=True,blank=True)
    def __str__(self):
        return self.name
class Product(models.Model):
    unique_id = models.CharField(max_length = 20, unique= True,editable=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(product_category, on_delete=models.PROTECT)
    brand_name = models.CharField(max_length=100, blank=True, null=True,unique=True)
    stock_quantity = models.PositiveIntegerField()
    is_new = models.BooleanField(default = False)
    image1 = models.ImageField(upload_to='product_image/',null=True,blank=True)
    image2 = models.ImageField(upload_to='product_image/',null=True,blank=True)
    image3 = models.ImageField(upload_to='product_image/',null=True,blank=True)
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    related_products = models.ManyToManyField('self', blank=True)
    def __str__(self):
        return self.brand_name
    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = uuid.uuid4().hex[:36]
        super().save(*args, **kwargs)

class Wishlist(models.Model):
    unique_id = models.CharField(max_length = 20, unique= True,editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)      
    def __str__(self):
        return f'{self.user.username} - {self.product.brand_name}'  
    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = uuid.uuid4().hex[:36]
        super().save(*args, **kwargs)
class Comment(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,null=True,blank=True)
    full_name = models.CharField(max_length = 50,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)        
    def __str__(self) -> str:
        return self.content
    