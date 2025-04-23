from django.urls import path
from . import views
from .views import place_order

app_name='cart'

urlpatterns = [
    path('add/<int:part_id>/', views.add_cart, name='add_cart'),
    path('', views.cart_detail, name='cart_detail'),
    path('remove/<int:part_id>/', views.cart_remove, name='cart_remove'),
    path('full_remove/<int:part_id>/', views.full_remove, name='full_remove'),
    path('new_order/',views.create_order,name='new_order'),
    path('place-order/', place_order, name='place_order'),
    path('resend-alerts/', views.resend_low_stock_alerts, name='resend_low_stock'),
]
