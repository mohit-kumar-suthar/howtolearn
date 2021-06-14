from django.db import models
from django.contrib.auth.models import User 
import uuid

class access_key(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    key = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.key = uuid.uuid4().hex[:16].upper()
        super(access_key, self).save(*args, **kwargs)

