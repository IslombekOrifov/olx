from django.urls import path

from .views import *


urlpatterns = [
    path('top/', ProductTopListAPIView.as_view()),
    path('detail/<int:pk>/', ProductRetriveAPIView.as_view()),

    path('destroy/category/<int:pk>/', CategoryDestroyAPIView.as_view()),
    path('category/', CategoryListAPIView.as_view()),
    path('fields/<int:category_id>/', FieldListAPIView.as_view()),

    path('', ProductListAPIView.as_view()),
]
