from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    email = models.EmailField()
    phone = models.CharField(max_length=12)

    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.username
    

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=225, null=True)
    description = models.CharField(max_length=500, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True, null=True)

    def __str__(self):
        return self.name
    
    def is_registered_before_2_month(self):
        return timezone.now() - self.created_at > timedelta(days=60)