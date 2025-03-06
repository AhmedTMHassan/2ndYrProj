from django.urls import path
from .views import CategoryPageView, BrandPageView, PartPageView, HomePageView, BrandsByCategoryView, PartsByBrandView, PartDetailView

app_name = 'shop'

urlpatterns = [
    path('', HomePageView.as_view(), name='base.html'),
    path('parts/', PartPageView.as_view(), name='part_list'),
    path('category/', CategoryPageView.as_view(), name='category_list'),
    path('brand/', BrandPageView.as_view(), name='brand_list'),
    path('brands/<uuid:pk>/', BrandsByCategoryView.as_view(), name='brands_by_category'),
    path('parts-by-brand/<uuid:pk>/', PartsByBrandView.as_view(), name='parts_by_brand'),
    path('part/<int:pk>/', PartDetailView.as_view(), name='part_detail'),
]