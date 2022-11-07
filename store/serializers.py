from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection


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



    
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']

    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = fields = ['id', 'title', 'slug', 'description', 'inventory', 'unit_price', 'collection']

    