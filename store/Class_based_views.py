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
# ------------------------------------------- CLASS BASED VIEWS ---------------------------------------------
# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------




class ProductList(APIView):
    def get(self, request):
        query_set = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(query_set, many=True, context={'request':request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
           

class ProductDetail(APIView):

    def get(self, request,pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(APIView):

    def get(self, request):
        queryset = Collection.objects.annotate(products_count = Count('products')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CollectionDetail(APIView):

    def get(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)


    def put(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)










