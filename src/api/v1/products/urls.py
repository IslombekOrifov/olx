from django.urls import path

from .views import *


urlpatterns = [
    path('top/', ProductClientListAPIView.as_view()),
    path('', ProductClientListAPIView.as_view()),
]
