from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator


from api.v1.accounts.models import CustomUser
from .services import upload_category_path, upload_product_path
from .enums import ProductStatus


class Category(models.Model):
    parent = models.ForeignKey('self', blank=True, related_name='children', null=True, on_delete=models.CASCADE)
    creator = models.ForeignKey(CustomUser, related_name='categories', blank=True, null=True, on_delete=models.SET_NULL)

    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to=upload_category_path, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.name = ' '.join(self.name.strip().split())
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Field(models.Model):
    categories = models.ManyToManyField(Category)
    creator = models.ForeignKey(
        CustomUser, related_name='category_fields', 
        null=True, on_delete=models.SET_NULL
    )

    name = models.CharField(max_length=150, unique=True)
    
    is_filter = models.BooleanField(default=False)
    is_main = models.BooleanField(default=False)
    is_checkbox = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.name = ' '.join(self.name.strip().split())
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    author = models.ForeignKey(CustomUser, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    title = models.CharField(max_length=100, validators=[MinLengthValidator(20)])
    description = models.TextField(max_length=9000, validators=[MinLengthValidator(80)])
    region = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    
    # images
    image_main = models.ImageField(upload_to=upload_product_path, blank=True, null=True)
    image1 = models.ImageField(upload_to=upload_product_path, blank=True, null=True)
    image2 = models.ImageField(upload_to=upload_product_path, blank=True, null=True)
    image3 = models.ImageField(upload_to=upload_product_path, blank=True, null=True)
    image4 = models.ImageField(upload_to=upload_product_path, blank=True, null=True)
    image5 = models.ImageField(upload_to=upload_product_path, blank=True, null=True)
    image6 = models.ImageField(upload_to=upload_product_path, blank=True, null=True)
    image7 = models.ImageField(upload_to=upload_product_path, blank=True, null=True)

    # prices 
    price = models.FloatField(default=0, validators=[MinValueValidator(0.0)])
    price_is_dollar = models.BooleanField(default=False)
    exchange = models.BooleanField(default=False)
    negotiable = models.BooleanField(default=False) # kelishiladi

    # Additional Information
    product_condition = models.BooleanField(default=True)
    auto_renewal = models.BooleanField(default=False)

    # contact
    email = models.EmailField(max_length=50, blank=True)
    phone = models.CharField(max_length=13, blank=True)
    
    views_count = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(max_length=3, choices=ProductStatus.choices(), default=ProductStatus.wt.name)
    is_deleted = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.title = ' '.join(self.title.strip().split())
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class ProductField(models.Model):
    field = models.ForeignKey(Field, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, related_name='cat_fields', on_delete=models.CASCADE)

    # first choice
    text = models.CharField(max_length=255, blank=True)

    # second Choice
    is_true = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.text = ' '.join(self.text.strip().split())
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.field.name




    