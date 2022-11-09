from django.db.models.aggregates import Count, Sum 
from django.db.models import Q, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response 
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.pagination import PageNumberPagination
from .models import Product, Collection, OrderItem, Review, Cart, CartItem, Customer
from rest_framework.mixins import CreateModelMixin , RetrieveModelMixin , UpdateModelMixin
from .serializers import ProductSerializer,\
                        CollectionSerializer,\
                        ReviewSerializer, \
                        CartSerializer, \
                        CartItemSerializer,\
                        AddCartItemSerializer,\
                        UpdateCartItemSerializer,\
                        CustomerSerializer
from .permissions import IsAdminOrReadOnly
                         
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
    permission_classes = [IsAdminOrReadOnly]


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
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)




class CartItemViewSet(ModelViewSet):

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
         return CartItem.objects.filter(cart_id = self.kwargs['cart_pk']).select_related('product').all()

    def get_serializer_context(self):
         return {'cart_id': self.kwargs['cart_pk']}


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]


    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (customer, state) = Customer.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET' :
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)




