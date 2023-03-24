from django.shortcuts import render

from rest_framework import (
    viewsets,
    permissions
)

from .models import MainComplaint, Complaint
from .serializers import MainComplaintSerializer, ComplaintSerializer


class MainComplaintViewset(viewsets.ModelViewSet):
    queryset = MainComplaint.objects.all()
    serializer_class = MainComplaintSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def perform_create(self, serializer):
        return serializer.save(creator=self.request.user)


class ComplaintViewset(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_permissions(self):
       if self.action == 'create':
           return [permission() for permission in [permissions.IsAuthenticated,]]
       return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        return serializer.save(client=self.request.user)
    
