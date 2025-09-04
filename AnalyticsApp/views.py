from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product


# Create your views here.

@api_view(['GET'])
def product_analytics(request, category, min_price, max_price):
    products = Product.object.filter(category__iexact=category, price__gte=min_price, price__lte=max_price)
    result = {
        "total_products": products.count(),
        "average_price":products.aggregate(models.Avg('price')),
        "total_stock_value":products.aggregate(total_stock_val=models.Sum(models.F('price')*models.F('stock)')))
        }
    
    return Response(result)
