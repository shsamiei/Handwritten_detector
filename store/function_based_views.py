from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.views import APIView
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404


# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------
# ------------------------------------------- FUNCTION BASED VIEWS ------------------------------------------
# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------



# django way : 
# def product_list(request):
#     return HttpResponse('ok')

# rest_framework way : 

@api_view(['GET', 'POST'])
def product_list(request):

    if request.method == 'GET':
        query_set = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(query_set, many=True, context={'request':request})
        return Response(serializer.data)

    elif request.method =='POST':
        serializer = ProductSerializer(data=request.data)

        # if serializer.is_valid():
        #     serializer.validated_data
        #     return Response('ok')
        # else : 
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # MORE CLEAN WAY : 

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET': 
        # product = Product.objects.get(pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)








@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(products_count = Count('products')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CollectionSerializer(data=serializer.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET','PUT', 'DELETE'])
def collection_detail(request,pk):
    collection = get_object_or_404(Collection, pk=pk)

    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)

    elif request.method == 'PUT': 
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


