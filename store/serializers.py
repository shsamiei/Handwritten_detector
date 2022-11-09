from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection, Review, Cart, CartItem
from django.db.models.aggregates import Count, Sum

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
        fields = ['id', 'title', 'slug', 'description', 'inventory', 'unit_price', 'collection']

    

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'date']
 
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
 
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'unit_price']



class CartItemSerializer(serializers.ModelSerializer):
    # to show the product with detail : 
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField('get_total_price')

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta: 
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']



class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True) 
    # to show items with details :
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField('get_total_price')

    def get_total_price(self, cart: Cart):
        return Sum([item.quantity * item.product.unit_price for item in cart.items.all()])
 
    class Meta: 
        model = Cart
        fields = ['id',  'items', 'total_price']

    total_price = serializers.IntegerField(read_only = True)



class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given id exist')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        
        try : 
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        
        return self.instance
            
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']



class UpdateCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ['quantity']
