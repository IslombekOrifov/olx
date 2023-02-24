from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q

from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token

from .models import CustomUser, UserLanguage, Experience
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
    

class UserLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLanguage
        fields = ['language', 'level']


class UserExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        exclude = ['user', 'date_created']


class UserSerializer(serializers.ModelSerializer):
    languages = UserLanguageSerializer(many=True, required=False)
    experiences = UserExperienceSerializer(many=True, required=False)
    date_joined = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)
    class Meta:
        model = CustomUser
        fields = (
            'username', 'first_name', 'last_name', 'email', 'phone', 'balance',
            'date_joined', 'about', 'birth_date', 'avatar', 'other_skills', 'hobby',
            'resume', 'edu1_name', 'edu1_direction', 'edu1_start_date', 'edu1_end_date',
            'edu1_now', 'edu2_name', 'edu2_direction', 'edu2_start_date', 'edu2_end_date',
            'edu2_now', 'licence_category', 'languages', 'experiences'
        )
        read_only_fields = ('languages', 'experiences')
        

class AuthorSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name' 'email', 'phone' 'avatar')



