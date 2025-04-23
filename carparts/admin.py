from django.contrib import admin
from .models import Part, Category, Brand

class PartAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock')
    search_fields = ('title', 'description')
    list_filter = ('category', 'brand')

# Register your models here.
admin.site.register(Part, PartAdmin)
admin.site.register(Category)
admin.site.register(Brand)