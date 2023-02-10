from rest_framework import serializers
from .models import Product, Category, ProductField, Field

# start categories 
class CategoryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        extra_kwargs = {
            'creator': {'read_only': True, 'required': False},
        }


class CategoryClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image', 'parent')
# end categories 


# start Field
class FieldAminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'
        read_only_fields = ['creator', 'date_created']
        extra_kwargs = {
            'creator': {'required': False}
        }

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['id', 'name', 'is_checkbox']
# end Field 


# start product list and detail
class ProductListSerializer(serializers.Serializer):
    class Meta:
        model = Product
        fields = (
            'title', 'image_main', 'price', 'price_is_dollar', 'region',
            'exchange', 'negotiable', 'product_condition', 'date_created'
        )


class ProductFieldSerializer(serializers.ModelSerializer):
    field = serializers.CharField(source="field.name")
    class Meta:
        model = ProductField
        exclude = ('product',)


class ProductDetailSerializer(serializers.ModelSerializer):
    fields = ProductFieldSerializer()
    class Meta:
        model = Product
        exclude = (
            'auto_renewal', 'status', 'is_deleted', 'date_updated', 
        )
# end product list and detail


# sart product create
class ProductFieldCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductField
        exclude = ('product',)
        

class ProductCreateSerializer(serializers.ModelSerializer):
    fields = ProductFieldCreateSerializer(many=True)
    class Meta:
        model = Product
        exclude = (
            'views_count', 'status', 'is_deleted', 'date_created', 'date_updated', 
        )
    
    def create(self, validated_data):
        pass

# end product create