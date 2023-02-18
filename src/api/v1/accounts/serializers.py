from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q

from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token

from .models import CustomUser
from .validators import validate_phone_and_email


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(validators=[validate_phone_and_email])
    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(default=False)
    
    def validate(self, attrs):
        is_staff = attrs['is_staff']
        if is_staff:
            user = self.context['request'].user
            if not user.is_authenticated:
                raise exceptions.NotAuthenticated()
            if not user.is_staff:
                raise exceptions.PermissionDenied()
            
        username = attrs['username']
        if '@' in username:
            attrs['email'] = username
        else:
            attrs['phone'] = username
        
        return attrs

    def create(self, validated_data):
        instance = CustomUser.objects.create_user(**validated_data)
        return instance
    


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)
    class Meta:
        model = CustomUser
        exclude = ['is_active', 'is_deleted', 'is_staff', 'password']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'avatar')