from django.urls import path
from . import views


urlpatterns = [
    path('products/analytics/', views.product_analytics),
]