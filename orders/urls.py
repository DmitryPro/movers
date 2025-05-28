from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('my/', views.my_orders, name='my_orders'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    # Staff URLs
    path('staff/orders/', views.staff_order_list, name='staff_order_list'),
    path('staff/orders/<int:order_id>/', views.staff_order_detail, name='staff_order_detail'),
    path('staff/orders/<int:order_id>/status/', views.staff_change_status, name='staff_change_status'),
]