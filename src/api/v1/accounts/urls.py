from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView

# from .views import ()

from .routers import router


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
]

urlpatterns += router.urls