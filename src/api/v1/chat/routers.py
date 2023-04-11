from rest_framework import (
    routers 
)


from .views import MessageAPIViewSet


router = routers.SimpleRouter()
router.register('', MessageAPIViewSet)

