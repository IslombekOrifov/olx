from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q

from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token

from .models import CustomUser
from .validators import validate_phone


class StaffRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'email', 'password']
    
    def validate(self, attrs):
        try:
            validate_email(attrs['username'])
            attrs['email'] = attrs['username']
        except:
            try:
                validate_phone(attrs['username'])
                attrs['phone'] = attrs['username']
            except:
                raise ValidationError('Enter valid email or phone number')
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.filter(
            Q(username=validated_data['username']) | Q(email=validated_data['username']) |
            Q(phone=validated_data['username']) 
            ).exists()
        if user:
            raise exceptions.ValidationError('This user already created')
        instance = CustomUser.objects.create_user(is_staff=True, **validated_data)
        return instance
    

class ClientRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        try:
            validate_email(attrs['username'])
            attrs['email'] = attrs['username']
        except:
            try:
                validate_phone(attrs['username'])
                attrs['phone'] = attrs['username']
            except:
                raise ValidationError('Enter valid email or phone number')
        return attrs


    def create(self, validated_data):
        user = CustomUser.objects.filter(
            Q(username=validated_data['username']) | Q(email=validated_data['username']) |
            Q(phone=validated_data['username']) 
            ).exists()
        if user:
            raise exceptions.ValidationError('This user already created')
        instance = CustomUser.objects.create_user(**validated_data)
        return instance

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)
    class Meta:
        model = CustomUser
        exclude = ['is_active', 'is_deleted', 'is_staff', 'password']



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(source='email', max_length=128)
    password = serializers.CharField(max_length=128, write_only=True)


    def validate(self, data):
        username = data.get('email')
        password = data.get('password')
        user = get_object_or_404(CustomUser, email=username)
        if not user.check_password(password):
            raise exceptions.NotFound()

        self.user = user
        return data

    
    def save(self, *args, **kwargs):
        return Token.objects.get_object_or_create(user_id=self.user.id).key


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'avatar')