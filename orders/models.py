from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from products.models import Product
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    unique_id = models.CharField(max_length = 20, unique= True,editable=False,null=True,blank=True)
    order_number = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    shipping_address = models.TextField()
    order_status = models.CharField(
        max_length=20, choices=ORDER_STATUS_CHOICES)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_method = models.TextField()
    def __str__(self):
        return self.order_number
    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = uuid.uuid4().hex[:36]
        super().save(*args, **kwargs)
class OrderItem(models.Model):
    unique_id = models.CharField(max_length = 20, unique= True,editable=False,null=True,blank=True)
    order = models.ForeignKey(Order,on_delete = models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField(null=False)
    def __str__(self):
        return self.product.brand_name
    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = uuid.uuid4().hex[:36]
        super().save(*args, **kwargs)
@receiver(post_save, sender=Order)
def update_product_stock(sender, instance, **kwargs):
    if instance.order_status == 'delivered':
        order_items = instance.orderitem_set.all()
        for order_item in order_items:
            product = order_item.product
            product.stock_quantity -= order_item.quantity 
            product.save()