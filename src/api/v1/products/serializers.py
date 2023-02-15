from rest_framework import serializers

from api.v1.accounts.serializers import AuthorSerializer

from .models import Product, Category, ProductField, Field


# start admin serializers
class CategoryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        extra_kwargs = {
            'creator': {'read_only': True, 'required': False},
        }

class FieldAminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'
        read_only_fields = ['creator', 'date_created']
        extra_kwargs = {
            'creator': {'required': False}
        }
# end admin serializers


# start client serializers
class CategoryChildsChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class CategoryChildrenSerializer(serializers.ModelSerializer):
    children = CategoryChildsChildrenSerializer(many=True)
    class Meta:
        model = Category
        fields = ('id', 'name', 'children')


class CategorySerializer(serializers.ModelSerializer):
    children = CategoryChildrenSerializer(many=True)
    class Meta:
        model = Category
        fields = ('id', 'name', 'image', 'children')


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['id', 'name', 'is_checkbox']


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'title', 'image_main', 'price', 'price_is_dollar', 'region',
            'exchange', 'negotiable', 'product_condition', 'date_created'
        )


class ProductFieldSerializer(serializers.ModelSerializer):
    field = serializers.StringRelatedField(source="field.name")
    class Meta:
        model = ProductField
        fields = ('field', 'text', 'is_true')


class ProductDetailSerializer(serializers.ModelSerializer):
    cat_fields = ProductFieldSerializer(many=True)
    author = AuthorSerializer()
    class Meta:
        model = Product
        fields = ( 
            'title', 'description', 'category', 'price', 'price_is_dollar', 
            'exchange', 'negotiable', 'product_condition', 'region', 'district',
            'image_main', 'image1', 'image2', 'image3', 'image4', 'image5',
            'image6', 'image7', 'email', 'phone', 'views_count', 'date_created',
            'cat_fields', 'author'
        )


class ProductFieldCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductField
        exclude = ('product',)
        

class ProductCreateSerializer(serializers.ModelSerializer):
    fields = ProductFieldCreateSerializer(many=True)
    class Meta:
        model = Product
        exclude = (
            'views_count', 'status', 'is_deleted', 
            'date_created', 'date_updated',
        )

# end client serializers