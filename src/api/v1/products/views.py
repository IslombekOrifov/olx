from rest_framework import (
    generics,
    permissions,
    authentication
)

from api.v1.accounts.permissions import IsDeleted
from .models import *
from .enums import ProductStatus
from .serializers import (
    CategoryAdminSerializer, CategoryClientSerializer, FieldAminSerializer,
    FieldSerializer, ProductListSerializer, ProductFieldSerializer, 
    ProductDetailSerializer, ProductFieldCreateSerializer, ProductCreateSerializer
)

# Create your views here.
class CategorAdminyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryAdminSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    authentication_classes = [authentication.BasicAuthentication]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class CategoryAdminRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryAdminSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    authentication_classes = [authentication.BasicAuthentication]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


class FieldAdminListCreateAPIView(generics.ListCreateAPIView):
    queryset = Field.objects.all(is_deleted=False)
    serializer_class = FieldAminSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    authentication_classes = [authentication.BasicAuthentication]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class FieldAdminRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Field.objects.all(is_deleted=False)
    serializer_class = FieldAminSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    authentication_classes = [authentication.BasicAuthentication]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


class CategoryClientListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(is_active=True, is_deleted=False)
    serializer_class = CategoryClientSerializer


class FieldClientListAPIView(generics.ListAPIView):
    queryset = Field.objects.filter(is_active=True, is_deleted=False)
    serializer_class = FieldSerializer
    permission_classes = [permissions.IsAuthenticated, ~IsDeleted]
    authentication_classes = [authentication.BasicAuthentication]


class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.filter(status=ProductStatus.ac.name, is_deleted=False)
    serializer_class = ProductCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.BasicAuthentication]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class ProductClientListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(status=ProductStatus.ac.name, is_deleted=False)
    serializer_class = ProductListSerializer

