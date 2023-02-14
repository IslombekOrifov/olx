from rest_framework import (
    views,
    generics,
    permissions,
    authentication
)


class WishlistAddApiView(generics.CreateAPIView):
    
