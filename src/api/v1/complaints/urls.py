from django.urls import path

from .views import *
from .routers import router


urlpatterns = [

]

urlpatterns += router.urls
