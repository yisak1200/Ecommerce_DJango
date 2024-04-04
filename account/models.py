from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class user_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_phone_number = models.CharField(max_length=15, null=True, blank=True)
    user_address = models.CharField(max_length=200, blank=True, null=True)
    email_token = models.CharField(max_length=200, blank=True, null=True)
    is_verified = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.user.username
