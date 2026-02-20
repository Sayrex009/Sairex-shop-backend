from rest_framework import viewsets, permissions
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.AllowAny]


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.select_related('product').all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.AllowAny]
