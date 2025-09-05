from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Avg, Sum,F
from .models import Product
from decimal import Decimal
from django.core.cache import cache


# Create your views here.

@api_view(['GET'])
def product_analytics(request):
    category = request.GET.get('category', '').strip()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    filters = {}
    if category:
        filters['category__iexact'] = category
    if min_price is not None:
        filters['price__gte'] = Decimal(str(min_price))
    if max_price is not None:
        filters['price__lte'] = Decimal(str(max_price))
    
    cache_key = f"product_analytics:{category}:{min_price}:{max_price}"
    result = cache.get(cache_key)
    if not result:
        products = Product.objects.filter(**filters)
        total_products = products.count()
        avg_price = products.aggregate(avg=Avg('price'))['avg']
        total_stock_value = products.aggregate(val=Sum(F('price') * F('stock')))['val']
        result = {
            "total_products": total_products,
            "average_price": round(avg_price or 0, 2),
            "total_stock_value": float(total_stock_value or 0)
        }
        cache.set(cache_key, result, 300)  # Cache for 5 minutes
    return Response(result)
