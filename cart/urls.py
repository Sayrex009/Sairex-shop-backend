from rest_framework import routers
from .views import CartViewSet, CartItemViewSet

router = routers.DefaultRouter()
router.register(r'', CartViewSet, basename='cart')
router.register(r'items', CartItemViewSet, basename='cartitem')

urlpatterns = router.urls
