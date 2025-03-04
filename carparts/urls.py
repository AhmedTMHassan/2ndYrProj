from django.urls import path
from .views import CategoryPageView, BrandPageView, PartPageView, HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='base.html'),
    path('parts/', PartPageView.as_view(), name='part_list'),
    path('category/', CategoryPageView.as_view(), name='category_list'),
    path('brand/', BrandPageView.as_view(), name='brand_list'),
    
]