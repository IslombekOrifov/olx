from rest_framework import (
    routers 
)


from .views import (
    UserAPIViewSet, UserLanguageAPIViewSet, UserExperienceAPIViewSet,   
    UserAdminAPIViewSet
)


router = routers.SimpleRouter()
router.register('adminuser/action', UserAdminAPIViewSet, basename='adminuser')
router.register('user/languages', UserLanguageAPIViewSet)
router.register('user/experiences', UserExperienceAPIViewSet)
router.register('', UserAPIViewSet, basename='users')
