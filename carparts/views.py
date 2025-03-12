from django.views.generic import ListView, TemplateView, DetailView
from .models import Part, Brand, Category
from django.core.paginator import Paginator
from django.shortcuts import render

class HomePageView(TemplateView):
    template_name = 'base.html'

class CategoryPageView(ListView):
    model = Category
    template_name = 'shop/category.html'
    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand_list'] = Brand.objects.all()  
        context['part_list'] = Part.objects.all()    
        return context

class BrandPageView(ListView):
    model = Brand
    template_name = 'shop/brand.html'
    context_object_name = 'brand_list'
    

class PartPageView(ListView):
    model = Part
    template_name = 'shop/part.html'  
    context_object_name = 'part_list' 
    paginate_by = 6  # Number of parts per page

    def get_queryset(self):
        # Get all parts available (with stock > 0) - adjust this as per your requirement
        queryset = Part.objects.all()  # Filtering based on stock > 0
        return queryset

class BrandsByCategoryView(DetailView):
    model = Category
    template_name = 'brands_by_category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        brands = Brand.objects.filter(category=category)
        context['brands'] = brands
        return context
    
class PartsByBrandView(DetailView):
    model = Brand
    template_name = 'parts_by_brand.html'
    context_object_name = 'brand'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = self.object
        parts = Part.objects.filter(brand=brand)
        context['parts'] = parts
        return context

class PartDetailView(DetailView):
    model = Part
    template_name = 'part_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand_list'] = Brand.objects.all() 
        return context
    