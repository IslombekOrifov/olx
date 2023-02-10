from rest_framework import (
    generics,
    permissions,
    authentication
)
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django.db.models import Q

from api.v1.accounts.permissions import IsDeleted
from api.v1.tariffs.enums import AdvantageType
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
    queryset = Field.objects.all()
    serializer_class = FieldAminSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    authentication_classes = [authentication.BasicAuthentication]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class FieldAdminRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldAminSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    authentication_classes = [authentication.BasicAuthentication]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


class CategoryClientListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(is_active=True)
    serializer_class = CategoryClientSerializer


class FieldClientListAPIView(generics.ListAPIView):
    queryset = Field.objects.filter()
    serializer_class = FieldSerializer
    permission_classes = [permissions.IsAuthenticated, ~IsDeleted]
    authentication_classes = [authentication.BasicAuthentication]


class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.filter(status=ProductStatus.ac.name, is_deleted=False)
    serializer_class = ProductCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.BasicAuthentication]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ProductClientListAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('category',)

    def get_queryset(self):
        queryset = Product.objects.filter(
            status=ProductStatus.ac.name, 
            is_deleted=False
        ).order_by('-date_created')
        return queryset


class ProductClientListAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('category',)

    def get_queryset(self):
        queryset = Product.objects.filter(
            Q(tariffs__tariff__advantages__advantage_type=AdvantageType.t.name) |
            Q(tariffs__tariff__advantages__advantage_type=AdvantageType.t.name),
            status=ProductStatus.ac.name, 
            is_deleted=False,
            
        ).order_by('-date_created')
        return queryset

    def list(self, request, *args, **kwargs):
        page = request.query_params.get('page', 1)
        queryset = self.filter_queryset(self.get_queryset())[(page - 1) * 3][:3]
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

