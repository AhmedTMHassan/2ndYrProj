from django.db import models
import uuid
from django.core.mail import send_mail
from django.conf import settings
# Create your models here.
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
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_stock = None

        if not is_new:
            old_stock = Part.objects.get(pk=self.pk).stock

        super().save(*args, **kwargs)

        if self.stock < 3 and (is_new or old_stock >= 3):
            self.send_low_stock_email()

    def send_low_stock_email(self):
        try:
            send_mail(
                subject=f"Low Stock Warning for {self.name}",
                message=f"The stock for part '{self.name}' is critically low: {self.stock}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
                html_message=f"""
                    <p>⚠️ <strong>Stock Alert</strong></p>
                    <p>The part <strong>{self.name}</strong> has dropped below the minimum stock level.</p>
                    <p>Current Stock: <strong>{self.stock}</strong></p>
                """
            )
        except Exception as e:
            print(f"Email failed: {e}")
    

