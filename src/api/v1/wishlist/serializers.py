from rest_framework import serializers
from accounts.models import CustomUser


class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'email', 'first_name', 'last_name', 'phone', 
        
        )