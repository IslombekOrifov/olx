from rest_framework import routers

from .views import (
    CategoryAdminViewSet
)

router = routers.SimpleRouter()

router.register('category/admin', CategoryAdminViewSet)