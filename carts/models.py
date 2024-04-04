from django.db import models
from django.contrib.auth.models import User
from products.models import Product
import uuid

class Cart(models.Model):
    unique_id = models.CharField(max_length = 20, unique= True,editable=False,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, blank=True, null=True)
    amount =models.PositiveIntegerField(null =True,blank=True)
    total_price=models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)

    def __str__(self):
        return f"Cart for {self.user.username}"
    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = uuid.uuid4().hex[:36]
        super().save(*args, **kwargs)