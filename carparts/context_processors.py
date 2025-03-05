from .models import Category, Part

def category_list(request):
    return {'category_list': Category.objects.all()}

def part_list(request):
    return {'part_list': Part.objects.all()}