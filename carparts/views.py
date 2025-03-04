from django.views.generic import ListView
from .models import Part, Brand, Category

class CategoryPageView(ListView):
    model = Category
    template_name = 'shop/category.html'
    context_object_name = 'category_list'

class BrandPageView(ListView):
    model = Brand
    template_name = 'shop/brand.html'
    context_object_name = 'brand_list'

class PartPageView(ListView):
    model = Part
    template_name = 'shop/part.html'
    context_object_name = 'part_list'