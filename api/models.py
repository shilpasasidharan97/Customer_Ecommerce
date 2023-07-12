from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    email = models.EmailField()
    phone = models.CharField(max_length=12)

    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.username