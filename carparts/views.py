from django.views.generic import ListView, TemplateView, DetailView
from .models import Part, Brand, Category
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render

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
    paginate_by = 6  
    

class PartPageView(ListView):
    model = Part
    template_name = 'shop/part.html'  
    context_object_name = 'part_list' 
    paginate_by = 6  

    def get_queryset(self):
        sort = self.request.GET.get('sort', 'title_asc')  # Default sorting: alphabetical (A-Z)
        queryset = Part.objects.all()

        # Apply sorting
        if sort == 'price_asc':
            queryset = queryset.order_by('price')  # Low to high
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')  # High to low
        elif sort == 'title_desc':
            queryset = queryset.order_by('-title')  # Z-A
        else:  # Default: title_asc
            queryset = queryset.order_by('title')  # A-Z

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort', 'title_asc')  # Pass the current sorting option
        return context
    
    

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
        categories = brand.category.all()
        context['category'] = categories.first() if categories.exists() else None
        return context

class PartDetailView(DetailView):
    model = Part
    template_name = 'part_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand_list'] = Brand.objects.all() 
        return context
    