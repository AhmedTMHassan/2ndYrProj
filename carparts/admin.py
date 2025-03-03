from django.contrib import admin
from .models import Part, Category, Brand

# Register your models here.
admin.site.register(Part)
admin.site.register(Category)
admin.site.register(Brand)