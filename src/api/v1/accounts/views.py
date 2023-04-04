from django.http import Http404
from django.core.exceptions import ValidationError

from rest_framework import (
    generics,
    permissions,
    authentication,
    status,
    exceptions,
    viewsets,
    views,
    routers,
    mixins
)
from rest_framework.response import Response

from .permissions import IsDeleted
from .models import CustomUser, UserLanguage, Experience
from .serializers import (
    RegisterSerializer, UserSerializer, UserLanguageSerializer,
    UserExperienceSerializer, AuthorSerializer, UserAdminListSerializer,
    UserAdminUpdateASerializer
)

class UserAdminAPIViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'username'

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterSerializer
        if self.action == 'list':
            return UserAdminListSerializer
        if self.action == 'retrieve':
            return UserSerializer
        if self.action == 'update':
            return UserAdminUpdateASerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [permission() for permission in []]
        return [permission() for permission in self.permission_classes]
    
    
    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        obj = CustomUser.objects.filter(is_deleted=False, **filter_kwargs).prefetch_related(
            'languages', 'experiences').get()
        if not obj:
            raise Http404('No matches the given query.')
        
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        
        return obj
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save()


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
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_object()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.filter(is_active=True, is_deleted=False)
    serializer_class = AuthorSerializer
