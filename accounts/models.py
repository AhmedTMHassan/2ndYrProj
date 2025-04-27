from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model
from django.urls import reverse


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True, blank=True)


 

class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        null=True,
        on_delete=models.CASCADE,
        )
    email = models.EmailField(blank=False, null=False)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('show_profile', args=[str(self.id)])
