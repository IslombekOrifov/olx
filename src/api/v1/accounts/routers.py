from rest_framework import (
    routers 
)


from .views import (
    UserAPIViewSet, UserLanguageAPIViewSet, UserExperienceAPIViewSet
)


router = routers.SimpleRouter()
router.register('user/languages', UserLanguageAPIViewSet)
router.register('user/experiences', UserExperienceAPIViewSet)
router.register('', UserAPIViewSet, basename='users')
