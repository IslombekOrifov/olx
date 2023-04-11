from django.urls import path

from .views import *


urlpatterns = [
    path('wishlist/delete/<int:id>/', WishlistDestroyApiView.as_view()),
    path('wishlist/add/', WishlistAddApiView.as_view()),
    path('wishlist/list/', WishlistListApiView.as_view()),

    path('follow/delete/<int:id>/', FollowDestroyApiView.as_view()),
    path('follow/add/', FollowAddApiView.as_view()),
    path('follow/list/', FollowListApiView.as_view()),
   
]
