from rest_framework import serializers

from api.v1.accounts.models import CustomUser
from .models import Wishlist, Follow


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['product',]


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['seller',]

    def create(self, validated_data):
        validated_data['seller'] = CustomUser.objects.get(username=validated_data['seller']).id
        follow = Follow.objects.create(**validated_data)
        return follow