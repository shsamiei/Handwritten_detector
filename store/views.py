from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404

# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------
# ------------------------------------------- GENERIC VIEWS -------------------------------------------------
# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------




class ProductList(ListCreateAPIView):

    # if you some logics for creating  queryset or serializer you should use this methods 

    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()

    # def get_serializer_class(self):
    #     return ProductSerializer

    # otherwise you can use queryset and serializerclass just like we have below :

    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request':self.request}

        
class ProductDetail(RetrieveUpdateDestroyAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0 :
                return Response({'error':'product cant be deleted '})
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(ListCreateAPIView):

    queryset = Collection.objects.annotate(products_count = Count('products')).all()
    serializer_class = CollectionSerializer
    
 
class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    # in the product_detail we had some logics for deleting an objects so we override the delete function
    # but here we don't have special logic for delete , put , get so we just set queryset and serializer_class 

    










