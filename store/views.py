from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from .models import Product, Collection, OrderItem, Review
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404

# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------
# ----------------------------------------------- View Set --------------------------------------------------
# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_serializer_context(self):
        return {'request':self.request}

    def destroy(self, request, *args, **kwargs):
        if Review.objects.filter(product_id=kwargs['pk']).count() > 0 :
                return Response({'error':'product cant be deleted '})
        return super().destroy(request, *args, **kwargs)



class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count = Count('products')).all()
    serializer_class = CollectionSerializer


# Modelviewset contain all the operators such as get post put delete etc. 
# if we dont want all of them and just get , delete we can inherit from ReadOnlyModelViewSet

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer



    










