from datetime import date
import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from sqlalchemy import Column, Integer, String, create_engine, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    public_visibility = models.BooleanField(default=True)  
    address = models.CharField(unique=False, max_length=100)
    birthdate = models.DateTimeField(null=True)
    number = models.CharField(_("number"), max_length=13)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    book = models.FileField(upload_to="book/pdf", max_length=250, null=True, default=None)
    description = models.TextField()
    visibility = models.BooleanField()
    cost = models.IntegerField()
    year_of_published = models.IntegerField(null=True) 
    user_id = models.IntegerField(null=False, default=None)

class Code(models.Model):
    number = models.CharField(max_length=5, blank=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)
    
    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]
        code_items = []

        for i in range(5):
            num = random.choice(number_list)
            code_items.append(num)

        code_string = "".join(str(item) for item in code_items)
        self.number = code_string
        super().save(*args, **kwargs)