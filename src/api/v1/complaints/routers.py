from rest_framework import routers

from .views import (
    MainComplaintViewset, ComplaintViewset 
)

router = routers.SimpleRouter()

router.register('base/complaint/admin', MainComplaintViewset)
router.register('users/complaint', ComplaintViewset)