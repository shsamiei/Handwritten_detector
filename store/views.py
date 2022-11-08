from django.db.models.aggregates import Count, Sum 
from django.db.models import Q, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response 
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from .models import Product, Collection, OrderItem, Review, Cart, CartItem
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer
from .filters import ProductFilter

# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------
# ----------------------------------------------- View Set --------------------------------------------------
# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------

class ProductViewSet(ModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['collection_id']
    filterset_class = ProductFilter
    # pagination_class = PageNumberPagination
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']


    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None : 
    #             queryset = Product.objects.filter(collection_id = collection_id)
    #     return queryset

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
    serializer_class = ReviewSerializer

    def get_queryset(self):
         return Review.objects.filter(product_id = self.kwargs['product_pk'])

    def get_serializer_context(self):
         return {'product_id': self.kwargs['product_pk']}


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.annotate(
            total_price = Sum(F('items__quantity'))
         ).all()
    serializer_class = CartSerializer




class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
         return CartItem.objects.filter(cart_id = self.kwargs['cart_pk']).all()

    # def get_serializer_context(self):
    #      return {'cart_id': self.kwargs['cart_pk']}


#------------------begin-----------------------------
    # Customers and the total amount they’ve spent

    # query_set = Customer.objects.annotate(
    #      total_spent = Sum(F('order__orderitem__unit_price') * F('order__orderitem__quantity')),
    #      quantity = F('order__orderitem__quantity')
    # )
#-------------------end------------------------------
     





