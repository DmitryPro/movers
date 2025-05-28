from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from moving_company.views_signup import signup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('orders/', include('orders.urls')),
    path('signup/', signup, name='signup'),
    path('', RedirectView.as_view(pattern_name='orders:create_order', permanent=False)),
    path('', include('django.contrib.auth.urls')),
]
