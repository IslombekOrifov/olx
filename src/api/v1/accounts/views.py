from django.http import Http404
from django.core.exceptions import ValidationError

from rest_framework import (
    generics,
    permissions,
    authentication,
    status,
    exceptions,
    viewsets,
    routers
)
from rest_framework.response import Response

from .permissions import IsDeleted
from .models import CustomUser, UserLanguage, Experience
from .serializers import (
    RegisterSerializer, UserSerializer, UserLanguageSerializer,
    UserExperienceSerializer, AuthorSerializer
)


class UserAPIViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(is_active=True, is_deleted=False)
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [permission() for permission in []]
        return [permission() for permission in self.permission_classes]
    
    def get_object(self):
        obj = CustomUser.objects.filter(
            id=self.request.user.id
        ).prefetch_related('languages', 'experiences').get()
        return obj

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save()


class UserLanguageAPIViewSet(viewsets.ModelViewSet):
    queryset = UserLanguage.objects.all()
    serializer_class = UserLanguageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()


class UserExperienceAPIViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = UserExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()
