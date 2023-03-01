from rest_framework import (
    serializers,
    utils
)

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


class ProductFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductField
        fields = ('id', 'field', 'product', 'text', 'is_true')



class ProductFieldCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = ProductField
        fields = ('id', 'field', 'product', 'text', 'is_true')
    extra_kwargs = {
        'id': {'required': False}
    }
    
    def update(self, instance, validated_data, product_id=None, field_id=None):
        serializers.raise_errors_on_nested_writes('update', self, validated_data)
        info = utils.model_meta.get_field_info(instance)

        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                pass
            else:
                if attr == 'field' or attr == 'product':
                    pass
                else:
                    setattr(instance, attr, value)

        instance.save()

        return instance

class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    cat_fields = ProductFieldCreateSerializer(many=True)
    id = serializers.IntegerField()
    class Meta:
        model = Product
        fields = ( 
            'id', 'title', 'description', 'category', 'region', 'district',
            'image_main', 'image1', 'image2', 'image3', 'image4', 
            'image5', 'image6', 'image7', 'price', 'price_is_dollar',
            'exchange', 'negotiable', 'product_condition', 'auto_renewal',
            'email', 'phone', 'cat_fields', 'author'
        )
        read_only_fields = ('author',)
        extra_kwargs = {
            'id': {'required': False}
        }

    def create(self, validated_data):
        cat_fields = validated_data.pop('cat_fields')
        product = Product.objects.create(**validated_data)
        if cat_fields:
            fields_gen = list((ProductField(product=product, **field) for field in cat_fields))
            ProductField.objects.bulk_create(fields_gen)
        return product

    def update(self, instance, validated_data):

        cat_fields = validated_data.pop('cat_fields')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if cat_fields:
            instance_fields = {field.id: field for field in instance.cat_fields.all()}
            validated_fields = {item['id']: item for item in cat_fields}

        new_data = []
        for field_id, data in validated_fields.items():
            field = instance_fields.get(field_id, None)
            if field is None:
                ProductFieldCreateSerializer.create(data)
            else:
                ProductFieldCreateSerializer.update(
                    self, instance=field, validated_data=data,
                    product_id=instance.id, field_id=field.id
                )
        if not self.partial:
            for field_id, field in instance_fields.items():
                if field_id not in validated_fields:
                    field.delete()

        return instance


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'title', 'image_main', 'price', 'price_is_dollar', 'region',
            'exchange', 'negotiable', 'product_condition', 'date_created'
        )


class ProductFieldDetailSerializer(serializers.ModelSerializer):
    field_title = serializers.StringRelatedField(source="field.name")
    class Meta:
        model = ProductField
        fields = ('id', 'field', 'field_title', 'product', 'text', 'is_true')


class ProductDetailSerializer(serializers.ModelSerializer):
    cat_fields = ProductFieldDetailSerializer(many=True)
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




# end client serializers
