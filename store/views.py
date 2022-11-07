from rest_framework.decorators import api_view
from rest_framework.response import Response 
from .models import Product
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404
# django way : 
# def product_list(request):
#     return HttpResponse('ok')

# rest way : 

@api_view()
def product_list(request):
    return Response('ok')


@api_view()
def product_detail(request, id):
    # product = Product.objects.get(pk=id)
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


