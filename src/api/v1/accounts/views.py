from rest_framework import (
    generics,
    permissions,
    authentication,
    status
)
from rest_framework.response import Response

from .permissions import IsDeleted
from .models import CustomUser
from .serializers import (
    RegisterSerializer, UserSerializer
)

# Create your views here.

class RegisterAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.filter(is_deleted=False)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsDeleted]

    def get_object(self):
        return self.request.user
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()



