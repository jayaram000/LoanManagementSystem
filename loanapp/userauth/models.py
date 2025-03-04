from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = (('user','User'),('admin','Admin'))
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default='user')
    otp = models.CharField(max_length=6,blank=True,null=True)
    is_verified = models.BooleanField(default=False)


    def __str__(self):
        return self.username

