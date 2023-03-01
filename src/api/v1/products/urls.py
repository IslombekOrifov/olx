from django.urls import path

from .views import *
from .routers import router


urlpatterns = [
    path('top/', ProductTopListAPIView.as_view()),
    path('detail/<int:pk>/', ProductRetriveAPIView.as_view()),

    path('category/', CategoryListAPIView.as_view()),
    path('fields/category/<int:pk>/', FieldListAPIView.as_view()),


    path('detail/<int:pk>/', ProductRetriveAPIView.as_view()),
    path('update/<int:pk>/', ProductUpdateAPIView.as_view()),
    path('create/', ProductCreateAPIView.as_view()),

    path('', ProductListAPIView.as_view()),

]

urlpatterns += router.urls
