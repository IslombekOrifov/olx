from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import Http404
from django.db.models import Q, F
from django.db.models.functions import JSONObject

from rest_framework import (
    views,
    generics,
    permissions,
    viewsets,
    authentication,
    status
)
from rest_framework.response import Response
from django_filters import rest_framework as filters


from api.v1.accounts.permissions import IsDeleted
from api.v1.tariffs.enums import AdvantageType

from .models import *
from .enums import ProductStatus
from .serializers import (
    CategoryAdminSerializer, CategorySerializer, FieldAminSerializer,
    FieldSerializer, ProductListSerializer, ProductFieldSerializer, 
    ProductDetailSerializer, ProductFieldCreateSerializer, ProductCreateUpdateSerializer
)


# start admin views
class CategoryAdminViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryAdminSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


class FieldAdminViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldAminSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
# end products admin

# product client
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(
        is_active=True, is_deleted=False, parent__isnull=True
    ).prefetch_related('children', 'children__children')
    serializer_class = CategorySerializer


class FieldListAPIView(generics.ListAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    # permission_classes = [permissions.IsAuthenticated, ~IsDeleted]
    lookup_field = 'pk'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        filter_kwargs = {'categories__id': self.kwargs[lookup_url_kwarg]}
        
        queryset = queryset.filter(**filter_kwargs)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.filter(status=ProductStatus.ac.name, is_deleted=False)
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    lookup_field = 'custom_id'
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('category',)

    def get_queryset(self):
        queryset = Product.objects.filter(
            status=ProductStatus.wt.name, is_deleted=False
        ).order_by('-date_created')
        return queryset


class ProductTopListAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('category',)


    def get_queryset(self):
        queryset = Product.objects.filter(
            Q(tariffs__tariff__advantages__advantage_type=AdvantageType.t.name) |
            Q(tariffs__advantages__advantage_type=AdvantageType.t.name),
            status=ProductStatus.ac.name, 
            is_deleted=False,
        ).order_by('-date_created')
        return queryset

    def list(self, request, *args, **kwargs):
        if not self.get_queryset():
            return Response('no')
        page = request.query_params.get('page', 1)
        queryset = self.filter_queryset(self.get_queryset())[(page - 1) * 3][:3]
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductRetriveAPIView(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        obj = Product.objects.filter(
            is_deleted=False, **filter_kwargs
        ).prefetch_related('cat_fields').select_related('author').get()
        if not obj:
            raise Http404('No matches the given query.')
        return obj


class ProductUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProductCreateUpdateSerializer

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        obj = Product.objects.filter(is_deleted=False, **filter_kwargs).prefetch_related('cat_fields').get()
        if not obj:
            raise Http404('No matches the given query.')
        
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        
        return obj

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class ProductDestroyAPIView(generics.DestroyAPIView):
    queryset = Product.objects.filter(is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

# end products client
