from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related('user')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
