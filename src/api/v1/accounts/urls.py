from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (
    StaffRegisterAPIView, ClientRegisterAPIView, 
    UserRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    
    path('register/staff/admin/', StaffRegisterAPIView.as_view()),
    path('register/client/', ClientRegisterAPIView.as_view()),


    path('user/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view())
]