from django.urls import path
from . import views


urlpatterns = [
    path('products/analytics/<str:category>&<int:min_price>&<int:max_price>/',views.product_analytics),
]