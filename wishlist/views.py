from rest_framework import viewsets, permissions
from .models import Wishlist, WishlistItem
from .serializers import WishlistSerializer, WishlistItemSerializer


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]


class WishlistItemViewSet(viewsets.ModelViewSet):
    queryset = WishlistItem.objects.select_related('product').all()
    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]
