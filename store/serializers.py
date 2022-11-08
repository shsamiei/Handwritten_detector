from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection, Review, Cart, CartItem
from django.db.models.aggregates import Count 

# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)

# class CollectionSerializer(serializers.ModelSerializer):
    # class Meta: 
        # model = Collection
        # avoid this , you may not expose every fields to client so avoid using __all__ it is for lazy developers
        # fields = '__all__'
        # fields = ['id', 'title']

# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
#     price_with_tax = serializers.SerializerMethodField('calculate_tax')

#     #primary_key
#     # collection = serializers.PrimaryKeyRelatedField(
#     #     queryset = Collection.objects.all()
#     # )

#     # String : 
#     # collection = serializers.StringRelatedField()

#     # nested_object:
#     # instead only getting the string title of collection we can have it as seriliazer : 
#     # collection = CollectionSerializer()

#     #Hyperlink:
#     collection = serializers.HyperlinkedRelatedField(
#         queryset = Collection.objects.all(),
#         view_name='collection-detail'
#     )

#     def calculate_tax(self, product: Product):
#         return product.unit_price * Decimal(1.1)

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta: 
#         model = Product
#         fields = ['id', 'title', 'slug', 'description', 'inventory', 'unit_price', 'collection']

#     # price_with_tax = serializers.SerializerMethodField('calculate_tax')

#     collection = serializers.HyperlinkedRelatedField(
#         queryset = Collection.objects.all(),
#         view_name='collection-detail'
#     )
#     def calculate_tax(self, product: Product):
#         return product.unit_price * Decimal(1.1)


    # it is a way to validate the data that we recieved from client : 

    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('passwords dont match')
    #     return data 

    # you can overwrite create method to add for example sth to the object 

    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1 
    #     product.save()
    #     return product

    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get('unit_price')
    #     instance.save()
    #     return instance


    #------------------begin-----------------------------
    # Collections and count of their products
    # query_set = Collections.objects.annotate(
    #     number_of_products = Count('product')
    # )
    #-------------------end------------------------------


    
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']
    
    # it is read only because it is just for serilizing and sent data to client and you can not post data and craete object with your product_count value 
    # omidvaram fahmide bashi :))) vali baz migam in baraye server be client gozashte shode , vaghti client dare post mikone in ro toye pocket nemizare pas 
    # read onlysh mikonim ke moshkeli ijad nashe :)) 
    
    products_count = serializers.IntegerField(read_only = True)

    
    
    # product_count = serializers.SerializerMethodField('product_count')
    # def product_count(self, collection: Collection):
    #     queryset =  Collection.objects.annotate(
    #         number_of_products = Count('product')
    #     )
    #     return queryset
        
    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = fields = ['id', 'title', 'slug', 'description', 'inventory', 'unit_price', 'collection']

    

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'date']
 
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
 


class CartSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Cart
        fields = ['id', 'created_at']

class CartItemSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CartItem
        fields = ['product', 'quantity']

    def create(self, validated_data):
        cart_id = self.context['cart_id']
        return Cart.objects.create(cart_id=cart_id, **validated_data)




