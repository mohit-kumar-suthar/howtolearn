from django.db import models
from django.contrib.auth.models import User
# Create your models here.


    
class register(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=255)
    joined_at = models.DateTimeField(auto_now_add=True)


