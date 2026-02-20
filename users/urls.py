from rest_framework import routers
from .views import UserViewSet, AddressViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'addresses', AddressViewSet)

urlpatterns = router.urls
