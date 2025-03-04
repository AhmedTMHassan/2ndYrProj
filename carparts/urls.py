from django.urls import path
from .views import CategoryPageView, BrandPageView, PartPageView

urlpatterns = [
    path('', CategoryPageView.as_view(), name='category_list'),
    path('brand/', BrandPageView.as_view(), name='brand_list'),
    path('part/', PartPageView.as_view(), name='part_list'),
]