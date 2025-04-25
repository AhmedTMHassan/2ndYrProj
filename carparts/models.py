from django.db import models
import uuid
from django.core.mail import send_mail
from django.conf import settings

class Category(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=250, unique=True)
    
    def __str__(self):
        return self.name

class Brand(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=250, unique=True)
    image = models.ImageField(upload_to='brand', blank=True)
    category = models.ManyToManyField(Category)
    
    
    def __str__(self):
        return self.name
        

class Part(models.Model):
    title = models.CharField(max_length=200)
    category = models.ManyToManyField(Category)
    brand = models.ManyToManyField(Brand)
    image = models.ImageField(upload_to='part', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    