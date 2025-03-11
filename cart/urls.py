from django.urls import path
from . import views

app_name='cart'

urlpatterns = [
    path('add/<int:part_id>/', views.add_cart, name='add_cart'),
    path('', views.cart_detail, name='cart_detail'),
    path('remove/<int:part_id>/', views.cart_remove, name='cart_remove'),
    path('full_remove/<int:part_id>/', views.full_remove, name='full_remove'),
]
