from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'user', 'provider', 'provider_payment_id', 'amount', 'currency', 'status', 'metadata', 'created_at')
