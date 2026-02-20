from rest_framework import routers
from .views import WishlistViewSet, WishlistItemViewSet

router = routers.DefaultRouter()
router.register(r'', WishlistViewSet, basename='wishlist')
router.register(r'items', WishlistItemViewSet, basename='wishlistitem')

urlpatterns = router.urls
