from rest_framework import (
    views,
    generics,
    permissions,
    authentication
)

from api.v1.products.models import Product
from api.v1.products.serializers import ProductListSerializer
from api.v1.accounts.models import CustomUser
from api.v1.accounts.serializers import AuthorSerializer

from .models import Wishlist, Follow
from .serializers import WishlistSerializer, FollowSerializer


class WishlistAddApiView(generics.CreateAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WishlistListApiView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        return Product.objects.filter(
            is_deleted=False,
            wishlists__user=self.request.user                         
        ).order_by('wishlists__date_created')
    

class WishlistDestroyApiView(generics.DestroyAPIView):
    queryset = Wishlist.objects.all()
    permission_classes = [permissions.IsAuthenticated,]




class FollowAddApiView(generics.CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FollowListApiView(generics.ListAPIView):
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        return CustomUser.objects.filter(
            is_active=True
            is_deleted=False,
            followers__user=self.request.user                         
        ).order_by('followers__date_created')
    

class FollowDestroyApiView(generics.DestroyAPIView):
    queryset = Follow.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
