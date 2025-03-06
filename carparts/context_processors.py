from .models import Category, Part, Brand

def category_list(request):
    return {'category_list': Category.objects.all()}

def part_list(request):
    return {'part_list': Part.objects.all()}

def brand_list(request):
    return {'brand_list': Brand.objects.all()}

