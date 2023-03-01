from django.shortcuts import render

from rest_framework import (
    viewsets,
    response
)
from django_filters import rest_framework as filters

from .models import Message
from .serializers import ChatSerializer

class ChatAPIViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all(is_deleted = False)
    serializer_class = ChatSerializer
    filter_backends = (filters.DjangoFilterBackend)
    filterset_fields = ('product',)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)