from django.db import models

# Create your models here.
class Part(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    description = models.CharField(max_length=255)