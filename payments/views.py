from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from .models import Payment
from .serializers import PaymentSerializer
from . import stripe as stripe_lib
from .tasks import process_stripe_event


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().select_related('user')
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]


class CreatePaymentIntentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        amount = request.data.get('amount')
        currency = request.data.get('currency', 'usd')
        order_id = request.data.get('order_id')
        if not amount:
            return Response({'detail': 'amount is required'}, status=status.HTTP_400_BAD_REQUEST)

        metadata = {'user_id': str(request.user.id)}
        if order_id:
            metadata['order_id'] = str(order_id)

        intent = stripe_lib.create_payment_intent(amount=amount, currency=currency, metadata=metadata)
        # persist Payment record tentatively
        Payment.objects.create(
            user=request.user,
            provider='stripe',
            provider_payment_id=intent.id,
            amount=amount,
            currency=currency,
            status='processing',
            metadata={'order_id': order_id} if order_id else {}
        )
        return Response({'client_secret': intent.client_secret})


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        payload = request.body.decode('utf-8')
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
        try:
            event = stripe_lib.construct_event(payload, sig_header)
        except Exception as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        # enqueue processing to Celery
        process_stripe_event.delay(event)

        return Response(status=status.HTTP_200_OK)
